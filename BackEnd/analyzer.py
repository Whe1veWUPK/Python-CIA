from py2neo import Graph, Node, Relationship, NodeMatcher,RelationshipMatcher
import astree
import sys
import ast_node_scanner
from FrontEnd import MainWindow
graph = Graph(MainWindow.neo_adr, auth=(MainWindow.neo_acc, MainWindow.neo_pwd))
node_matcher = NodeMatcher(graph)
print('start anal')
relation_matcher = RelationshipMatcher(graph)
"""影响集，里面存储的是影响到的节点的集合"""
impact_set = []

"""获得开始行并将其转化为 int 类型的数据"""
def get_start_line(node):
    return int(node['StartLine'])
"""单独为modify设立的"""
def for_modify(lines):
 
    #print(len(lines))
    for line in lines:
        #print(line)
        info_list = []
        #print("in")
        if line[0:13]=="FunctionDef :":
           # print("In func")
            info_list = line[14:].split(' ')
            node = graph.nodes.match("Function").where(Name=info_list[1],Path=info_list[0]).first()
            flag = 0
            if node in impact_set:
                impact_set.remove(node)
                flag = 1 
            #print("Success Matched")
            """更新开始行以及结束行"""
            update_data={
                'StartLine': info_list[3],                                        
                'EndLine': info_list[5] 
            }
            node.update(update_data)
            """更新到图里"""
            graph.push(node)  
            if flag == 1:
               impact_set.append(node)          
        if line[0:10]=="ClassDef :":
            #print("in class")

            info_list = line[11:].split(' ')
            node=graph.nodes.match("Class").where(Path=info_list[0],Name=info_list[1]).first()
            #print("success matched")
            flag = 0
            if node in impact_set:
                impact_set.remove(node)
                flag = 1 
            """更新开始行以及结束行"""
            update_data={
                'StartLine': info_list[3],                                        
                'EndLine': info_list[5] 
            }
            node.update(update_data)
            """更新到图里"""
            graph.push(node)
            if flag == 1:
                impact_set.append(node)
            
            
                
     
"""为增添修改设计所做的特殊的更新依赖图的函数 同时记录新添加的节点后进行返回"""
def update_graph(lines,target_index,nodes):
    """越过初始的文件节点 从下一个类或者函数节点开始"""
    if len(nodes)== 0:
        return 
    location = 1
    new_nodes=[]
    if target_index== len(nodes):
        """如果在末尾添加 则不需要更新任何节点 只需记录新节点"""
        for line in lines:
            info_list = []
            if line[0:13]=="FunctionDef :":
                info_list = line[14:].split(' ')
                node = graph.nodes.match("Function").where(Name=info_list[1],Path=info_list[0],StartLine=info_list[3],EndLine=info_list[5]).first()
                if node is None:
                    """节点为空 则说明是新节点"""
                    new_nodes.append(Node("Function",Path=info_list[0],Name=info_list[1],StartLine=info_list[3],EndLine=info_list[5]))
            if line[0:10]=="ClassDef :":
                info_list = line[11:].split(' ')
                node=graph.nodes.match("Class").where(Path=info_list[0],Name=info_list[1],StartLine=info_list[3],EndLine=info_list[5]).first()
                
                if node is None:
                    """节点为空 则说明是新节点"""
                    new_nodes.append(Node("Class",Path=info_list[0],Name=info_list[1],StartLine=info_list[3],EndLine=info_list[5]))
        return new_nodes
    for line in lines:
        info_list = []

        if line[0:13]=="FunctionDef :":

            info_list = line[14:].split(' ')
            if location < target_index:
                
                """如果在更新点之前则无需操作"""
                location += 1
                

                
            else:
                """如果该点需要更新 更新的点是已经存在的"""
                """确定的标志是名称 以及 路径相同 且图中存在"""

                
                node = nodes[location]
                
                if (node['Name']==info_list[1]) & (node['Path']==info_list[0]):

                    """路径 以及 名称 相同"""
                    node_to_be_update = graph.nodes.match().where(Name=info_list[1],Path=info_list[0]).first()
                    if node_to_be_update is not None:
                        """如果在图中找到 则说明确实是需要更新的节点"""
                        """更新开始行以及结束行"""
                        update_data={
                            'StartLine': info_list[3],                                        
                            'EndLine': info_list[5] 
                        }
                        node_to_be_update.update(update_data)
                        """更新到图里"""
                        graph.push(node_to_be_update)
                        """移动 location"""
                        location += 1

                    else:
                        """说明节点是新节点"""
                        """将新节点进行记录"""

                        new_nodes.append(Node("Function",Path=info_list[0],Name=info_list[1],StartLine=info_list[3],EndLine=info_list[5]))
                        """location 不移动"""
                else:
                    """说明路径名称都不一样 也是新节点"""

                    new_nodes.append(Node("Function",Path=info_list[0],Name=info_list[1],StartLine=info_list[3],EndLine=info_list[5]))
                    """location 不移动"""
        if line[0:10]=="ClassDef :":
            info_list = line[11:].split(' ')
            if location < target_index:
                """如果在更新节点之前则没有操作"""
                location += 1

            else:
                """如果该点需要更新 更新的点应该是已经在图中存在的"""
                """确定的标志是名称 路径 以及 该点已经在图中存在"""

                node = nodes[location]

                if (node['Name']==info_list[1]) & (node['Path']==info_list[0]):
                    """路径以及名称相同"""
                    node_to_be_update = graph.nodes.match().where(Name=info_list[1],Path=info_list[0]).first()
                    if node_to_be_update is not None:
                        """如果节点确实在图中存在"""
                        """则更新其开始行以及结束行"""
                        update_data={
                            'StartLine':info_list[3],
                            'EndLine': info_list[5]
                        }
                        node_to_be_update.update(update_data)
                        """向neo4j中进行同步"""
                        graph.push(node_to_be_update)
                        location += 1

                        """移动location"""
                    else:
                        """不在图中存在 说明是新节点"""
                        """将新节点进行记录"""

                        new_nodes.append(Node("Class",Path=info_list[0],Name=info_list[1],StartLine=info_list[3],EndLine=info_list[5]))
                        """location 不移动"""
                else:
                    """名称 路径不一样 说明也是新节点"""

                    new_nodes.append(Node("Class",Path=info_list[0],Name=info_list[1],StartLine=info_list[3],EndLine=info_list[5]))
                    """不需要移动Location"""
        """将新节点进行返回"""
    return new_nodes


                    



                
        

        

"""根据Ast 文件信息检索出坐标更改的点"""
def get_target_index(nodes,target_index,lines):
    """Location 从1 开始跳过文件路径"""
    limit =len(nodes)
    for line in lines:
        # print(line)
        if target_index >= limit:
            return target_index
        node = nodes[target_index]
        info_list = []
        if line[0:13]=="FunctionDef :":
           info_list = line[14:].split(' ')
           if node['StartLine'] == info_list[3] and node['Name']==info_list[1] and node['Path']==info_list[0]:
               """匹配 则更新target_index"""
               #print(node['StartLine'] +"=="+ info_list[3])
               target_index += 1
           else:
               #rint(line)
               return target_index
        if line[0:10]=="ClassDef :":
           info_list = line[11:].split(' ')
           if node['StartLine']==info_list[3] and node['Name']==info_list[1] and node['Path']==info_list[0]:
               """匹配 则更新target_index"""
               #print(node['StartLine'] +"=="+ info_list[3] )
               target_index += 1
           else:
               return target_index

class analyzer:
    def __init__(self,type,file_path,start_line,node_name):
        """构造函数 传入的参数依次为 修改类型 修改文件路径 修改节点开始行 修改的节点名称"""
        self.type = type
        self.file_path = file_path
        self.start_line = start_line
        self.node_name = node_name
    def analyze(self):
        """修改分析的启动函数"""
        if self.type == "Delete":
            """删除类型的修改分析"""
            self.delete_analyze()
        elif self.type == "Add":
            """增加类型的修改影响分析"""
            self.add_analyze()   
        elif self.type == "Modify":
           """修改类型的修改影响分析"""
           self.modify_analyze()
    
    def delete_analyze(self):
        global impact_set
        """清空影响集"""
        impact_set.clear()
        target_node = graph.nodes.match("Class",Path=self.file_path,Name=self.node_name,StartLine=self.start_line).first()
        
        """首先查找类节点"""

        if target_node is not None:
            
            """如果类节点不为空，将其加入影响集"""
            impact_set.append(target_node)

            """然后 找到所有的函数节点 （类的成员函数）"""
            includes_relations = list(relation_matcher.match([target_node],r_type='includes function'))
            function_nodes = []
            for relation in includes_relations:
                function_nodes.append(relation.end_node)
                
            """将所有找到的函数节点 加入影响集"""

            """接下来查找有call 类中函数的节点"""
            
            for node in function_nodes:
                call_relations = list(relation_matcher.match((None,node),r_type='calls'))
                for relation in call_relations:
                    """将有调用删除类中的节点加入影响集"""
                    impact_set.append(relation.start_node)    
            """对影响集进行去重处理 先转换为集合 后再次转换为列表"""
            impact_set =list(set(impact_set))
            """查询完成直接返回"""
            return 
        """类节点为空 则我们接下来在函数节点里搜索"""
        target_node = graph.nodes.match("Function",Path=self.file_path,Name=self.node_name,StartLine=self.start_line).first()

        # for node in nodes:
        #     print(node)
        # print(self.file_path+" "+self.node_name+" "+self.start_line)
        """如果删除的是函数节点"""
        if target_node is not None:
            """函数节点不为空 加入影响集"""
            impact_set.append(target_node)
            """获取所有调用该函数的节点"""
            call_relations = list(relation_matcher.match((None,target_node),r_type='calls'))
            for relation in call_relations:
                """将所有调用该函数节点的函数节点加入影响集"""
                impact_set.append(relation.start_node)
            
            """获取包含该函数的类节点"""
            includes_relations = list(relation_matcher.match((None,target_node),r_type='includes function'))
            for relation in includes_relations:
                """把文件节点筛选出去"""
                if relation.start_node['StartLine']!=0:
                   impact_set.append(relation.start_node)
            """对影响集进行去重处理 先转换为集合 后再次转换为列表"""
            impact_set = list(set(impact_set))
            """查询完成后直接返回"""
            return
        """其余情况 则说明待删除节点不存在 直接返回"""
        
        return 
    def add_analyze(self):
        """增加类型的修改影响分析"""
        global impact_set
        """清空影响集"""
        impact_set.clear()

        """首先根据添加节点的路径找到 所有该路径的节点 并按StartLine进行排序"""
        
        match_nodes = list(graph.nodes.match().where(Path=self.file_path).all())
        match_nodes.sort(key=get_start_line)
        # print("Matched Nodes: ")
        # for node in match_nodes:
        #     print(node)
        """接下来定位出增加的节点位置"""
        """首先重新 构造 ast输入到文件中"""
        f = open('ast.txt', 'w')
        f.seek(0)
        f.truncate()
         
        sys.stdout = f
 
        tree = astree.ast_constructor(self.file_path)
        visit = astree.my_visitor(self.file_path)
        visit.visit(tree)
        f.close()
        """获取Ast文件中的所有信息"""
        sys.stdout=sys.__stdout__
        f = open(r'ast.txt','r')
        f.seek(0)
        
        target_index = 1
        """获取target_index"""
        
        lines = ast_node_scanner.get_lines(r'ast.txt')
        target_index = get_target_index(match_nodes,target_index,lines)
        #print("Target Index: "+str(target_index))
        
        """更新图中已经存在节点的信息 同时获取新添加的节点集合"""
 
        new_nodes=update_graph(lines,target_index,match_nodes)

        """重新构建依赖图"""
        f.close()
        f = open(r'ast.txt','r')
        f.seek(0)
        ast_node_scanner.graph_constructor(r'ast.txt',1)
        f.close()
        f = open(r'ast.txt','r')
        f.seek(0)
        ast_node_scanner.graph_constructor(r'ast.txt',2)
        f.close()
        """计算影响集"""
        for node in new_nodes:
            """每个新添加的节点都是影响集"""
            impact_set.append(node)
        """影响集去重"""
        impact_set= list(set(impact_set))
        """结束程序"""
        return
    def modify_analyze(self):
        """修改类型的影响集计算"""
        """实际上就是先 删 后 增"""
        global impact_set
        """清空影响集"""
        impact_set.clear()
        """删修改分析"""

        self.delete_analyze()
        # for node in impact_set:
        #     print(node)
        """接下来是增修改分析"""
        """接下来定位出增加的节点位置"""
        """首先重新 构造 ast输入到文件中"""
        f = open('ast.txt', 'w')
        f.seek(0)
        f.truncate()
         
        sys.stdout = f
           
        tree = astree.ast_constructor(self.file_path)
        visit = astree.my_visitor(self.file_path)
        visit.visit(tree)
        f.close()
        """获取Ast文件中的所有信息"""
        sys.stdout=sys.__stdout__
        f = open(r'ast.txt','r')
        f.seek(0)
        
        f.close()
        lines = ast_node_scanner.get_lines(r'ast.txt')
        # for line in lines:
        #     print(line)
        # print("开始构建")
        for_modify(lines)
        """重新构建依赖图"""
        
        f = open(r'ast.txt','r')
        f.seek(0)
        ast_node_scanner.graph_constructor(r'ast.txt',1)
        f.close()
        f = open(r'ast.txt','r')
        f.seek(0)
        ast_node_scanner.graph_constructor(r'ast.txt',2)
        f.close()




        




# analy =analyzer("Add",r"D:\PythonProjects\Python-CIA\ForTest\forTest\test2.py",'4','test11')
# analyzer.analyze(analy)

# for node in impact_set:
#     print(node)