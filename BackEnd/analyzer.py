from py2neo import Graph, Node, Relationship, NodeMatcher,RelationshipMatcher
import astree
import sys
import ast_node_scanner
graph = Graph('bolt://localhost:7687', auth=('neo4j', '12345678'))
node_matcher = NodeMatcher(graph)
relation_matcher = RelationshipMatcher(graph)
"""影响集，里面存储的是影响到的节点的集合"""
impact_set = []



"""根据Ast 文件信息检索出坐标更改的点"""
def get_target_index(nodes,target_index,lines):
    """Location 从1 开始跳过文件路径"""
    for line in lines:
        print(line)
        info_list = []
        if line[0:13]=="FunctionDef :":
           print("FindFunction")
           info_list = line[13:].split(' ')
           if nodes[target_index]['StartLine'] == info_list[3]:
               """匹配 则更新target_index"""
               target_index += 1
           else:
               """不匹配则说明已经找到 直接退出"""
               return target_index
        elif line[0:10]=="ClassDef :":
           print("FindClass")
           info_list = line[10:].split(' ')
           if nodes[target_index]['StartLine']==info_list[3]:
               """匹配 则更新target_index"""
               target_index += 1
           else:
               """不匹配则说明已经找到 直接退出"""
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
    
    def delete_analyze(self):
        global impact_set
        """清空影响集"""
        impact_set.clear()
        target_node = graph.nodes.match("Class",Path=self.file_path,Name=self.node_name,StartLine=self.start_line).first()
        """首先查找类节点"""
        #print("进入")
   
            #print("未找到类节点")
        if target_node is not None:
            #print("进入")
            """如果类节点不为空，将其加入影响集"""
            impact_set.append(target_node)

            """然后 找到所有的函数节点 （类的成员函数）"""
            includes_relations = list(relation_matcher.match([target_node],r_type='includes function'))
            function_nodes = []
            for relation in includes_relations:
                function_nodes.append(relation.end_node)
                
            """将所有找到的函数节点 加入影响集"""
            for node in function_nodes:
                impact_set.append(node)
            # for node in impact_set:
            #     print(node)
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
        """如果删除的是函数节点"""
        if target_node is not None:
            #print ("是函数节点")
            """获取所有调用该函数的节点"""
            call_relations = list(relation_matcher.match((None,target_node),r_type='calls'))
            for relation in call_relations:
                """将所有调用该函数节点的函数节点加入影响集"""
                impact_set.append(relation.start_node)
            
            """获取包含该函数的类节点"""
            includes_relations = list(relation_matcher.match((None,target_node),r_type='includes function'))
            for relation in includes_relations:
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
        print("In add_analyze: ")
        """首先根据添加节点的路径找到 所有该路径的节点 并按StartLine进行排序"""
        
        match_nodes = graph.nodes.match().where(Path=self.file_path).order_by("_.startline")
        for node in match_nodes:
            print(node)
        """接下来定位出增加的节点位置"""
        """首先重新 构造 ast输入到文件中"""
        f = open('ast.txt', 'w')
        f.seek(0)
        f.truncate()
         
        sys.stdout = f
        sys.stderr = f
        tree = astree.ast_constructor(self.file_path)
        visit = astree.my_visitor(self.file_path)
        visit.visit(tree)
        """获取Ast文件中的所有信息"""
        sys.stdout=sys.__stdout__
        lines = ast_node_scanner.get_lines('ast.txt')
        
        target_index = 1
        """获取target_index"""
        
        print(len(lines))
        target_index = get_target_index(match_nodes,target_index,lines)

        print(target_index)
           



        




analy =analyzer("Add",r'D:\PythonProjects\Python-CIA\ForTest\forTest\test2.py','4','test11')
analyzer.analyze(analy)
for node in impact_set:
    print(node)

