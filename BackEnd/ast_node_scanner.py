

from py2neo import Graph, Node, Relationship, NodeMatcher,RelationshipMatcher
import os
import os.path
from FrontEnd import MainWindow
'''
用于搜索生成的节点信息文件
向neo4j中建立节点
包括函数节点，(包节点，类节点)
同时建立各个等级节点之间的调用情况
'''

graph = Graph(MainWindow.neo_adr, auth=(MainWindow.neo_acc, MainWindow.neo_pwd))
node_matcher = NodeMatcher(graph)
relation_matcher = RelationshipMatcher(graph)
print('start astr')

"""获取与某节点有关系的所有节点（一层）"""
def find_linked_nodes(node):
    linked_nodes = set()
    matched_relations = relation_matcher.match(nodes=(None,node))
    linked_nodes.update([relation.start_node for relation in matched_relations])
    matched_relations = relation_matcher.match(nodes=(node,None))
    linked_nodes.update([relation.end_node for relation in matched_relations])
    return linked_nodes



# 调用该函数即可直接开始建立
def graph_constructor(filename,round):
    """向neo4j中构建图的函数"""
    num_of_lines = get_text_lines(filename)
    lines = get_lines(filename)
    scan = my_scanner(num_of_lines,lines,filename,round)
    my_scanner.scan_driver(scan)


def get_text_lines(filename):
    """给定文件路径，计算文件行数的函数"""
    count = len(open(filename, 'r').readlines())
    return count


def get_lines(filename):
    """给定文件路径，读取文件中所有行的函数"""
    #print("in get_lines")
    f = open(filename,'r')
    # print("open file successfully")
    line = f.readline()
    #print(line)
    lines =[]
    while line:
        # print(line)
        line = line.strip('\n')
        lines.append(line)
        line=f.readline()
    # print(len(lines))
    f.close()
    return lines

def get_line(filename, line_num):
    """给定文件路径以及行数，返回该行的数据"""
    with open(filename, 'r') as f:
        for num, line in enumerate(f):
            if num == line_num:
                return line


def function_node_scanner(string):
    """首先要根据信息 判断该函数节点是否已经在数据库中建立"""
    info = string[14:]
    info_List = info.split(' ')
    function_node = None
    function_node = graph.nodes.match("Function",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
    if function_node is None:
        """如果没有在数据库中建立 则进行建立"""  
        function_node = Node("Function",Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
        graph.create(function_node)

def class_node_scanner(string):
    """给定类节点名称，在图中查找该节点是否已经建立"""
    info = string[11:]
    info_List = info.split(' ')
    class_node = None
    class_node=graph.nodes.match("Class",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
    if class_node is None: 
        """若没有则创建新节点"""
        class_node=Node("Class", Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
        graph.create(class_node)

class my_scanner:

    def __init__(self, num_of_lines,lines,filename,round):

        self.num_of_lines = num_of_lines
        self.filename = filename
        self.lines=lines
        self.location = 0
        self.round = round
        

    def scan_driver(self):
        if self.round == 1:
           """是第一轮 则建立节点"""
           """首先向数据库中建立 文件节点"""
           self.location = 0
           file_node = graph.nodes.match("File",Path=self.lines[self.location],StartLine=0).first()
           if file_node is None:
             file_node=Node("File",Path = self.lines[self.location],StartLine = 0)
             graph.create(file_node)
           self.location += 1
           """第一轮 建立节点(包括 函数 类)"""
           while self.location < self.num_of_lines:
               # string = get_line(self.filename, self.location)
               string = self.lines[self.location]
               if string[0:13]=="FunctionDef :":
                function_node_scanner(string)
               elif string[0:10]=="ClassDef :" :
                class_node_scanner(string)
               
               self.location = self.location + 1
        elif self.round==2:
           """是第二轮 则建立节点之间的关系"""
           self.location = 0 
           file_node = graph.nodes.match("File",Path=self.lines[self.location],StartLine=0).first()
           self.location = 1
       
           """第二轮 建立节点之间的关系"""
           while self.location < self.num_of_lines:
            #string = get_line(self.filename, self.location)
            
              string = self.lines[self.location]
              """如果是文件结构的第一层，将包节点与第一层的所有节点进行连接"""
              """这里的连接 包括文件节点与 类节点 以及 函数节点之间的连接"""
              if string[0:13]=="FunctionDef :":
                """建立文件节点与 第一层函数节点 之间的连接"""
                info = string[14:]
                info_List = info.split(' ')                
                function_node = graph.nodes.match("Function",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
                if function_node is None:
                    function_node = Node("Function",Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
                    graph.create(function_node)
                entity = Relationship(file_node,"includes function",function_node)
                graph.create(entity)
                self.function_relation_scanner(string,"Empty")
              elif string[0:6]=="Call :":
                self.scan_call(file_node)
              elif string[0:10]=="ClassDef :" :
                """建立文件节点 与 第一层类 节点之间的连接"""
                info = string[11:]
                info_List = info.split(' ')
                class_node = graph.nodes.match("Class",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
                if class_node == None:
                    
                    class_node = Node("Class",Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
                    graph.create(class_node)
                entity = Relationship(file_node,"includes class",class_node)
                graph.create(entity)
                self.class_relation_scanner(string, "Empty")
              else:
                self.location = self.location + 1
           
        
        
    
    def class_relation_scanner(self, string, node):
        if self.location >= self.num_of_lines:
            return None
        next_line = self.location + 1
        if next_line >= self.num_of_lines:
            return None 
        # father_class = get_line(self.filename, next_line)
        father_class = self.lines[next_line]
        info = string[11:]
        info_List = info.split(' ')
        """判断该类节点 是否有继承的父类"""
        if (father_class[0:6]=="Name :") and (string[0:10]=="ClassDef :"):
             """如果有继承的父类"""
             father_info = father_class[7:]
             father_Info_List = father_info.split(' ')
             father_node = graph.nodes.match("Class",Name=father_Info_List[1]).first()

             son_node = graph.nodes.match("Class",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
             if father_node is not None and son_node is not None:
               """建立子类 和 父类节点之间的关系"""
               entity = Relationship(father_node,"derives",son_node)
               graph.create(entity)

        if string[0:10]=="ClassDef :":
            if type(node) != type("a"):
                """如果当前已经是在一个类节点内了 则需要对类和类进行连接"""
                """这里的判断意思是 初始node的类型是一个 string 如果被赋予了Node 类型 则表示已经在一个类的节点内部了"""
                class_node = graph.nodes.match("Class",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
                if class_node is None :
                     """节点为空 则在neo4j 数据库中进行创建"""
                     class_node = Node("Class", Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
                     graph.create(class_node)
                """连接 两个类节点"""
                entity = Relationship(node, "includes class", class_node)
                graph.create(entity)   
            self.scan_class(string)
            
        elif string[0:13]=="FunctionDef :":
              if type(node) != type ("a") :
                  """如果当前已经是在一个类节点内 则需要对类和函数进行连接"""
                  """判断意思同上"""
                  class_node = node
                  function_info = string[14:]
                  info_List = function_info.split(' ')
                  function_node = graph.nodes.match("Function",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
                  if function_node is None :
                      """函数节点不存在则进行创建"""
                      function_node = Node("Function", Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
                      graph.create(function_node)
                  """连接 类节点 和 函数节点"""
                  entity = Relationship(class_node, "includes function", function_node)
                  graph.create(entity)
              self.scan_function(string)  
                        
        else:
            self.location = self.location + 1
           

        
    def scan_class(self, string):
        self.location = self.location + 1
        str_update = "Go"
        info = string[11:]
        info_List = info.split(' ')
        class_node = graph.nodes.match("Class",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
        if class_node is None :
            class_node = Node("Class", Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
            graph.create(class_node)
        while(str_update[0:10]!="EndClass :") and (self.location < self.num_of_lines) :
            # str_input = get_line(self.filename, self.location)
            str_input = self.lines[self.location]
            str_update = str_input
            self.class_relation_scanner(str_input, class_node)
        
        self.location -= 1


        
        


    def function_relation_scanner(self, string, node):
        
        if string[0:13]=="FunctionDef :":
            self.scan_function(string)
            
        elif string[0:6]=="Call :":  # 发现函数之间的调用关系
            self.scan_call(node)
           
        # elif string.find("Name") != -1:
        #     global graph
        #     if node != "Empty":
        #         name_node = Node("Name", name=string[7:])
        #         entity = Relationship(name_node, str(node.labels), node)
        #         graph.create(entity)
        #     else:
        #         name_node = Node("Name", name=string[7:])
        #         graph.create(name_node)
        elif string[0:10]=="ClassDef :":
             function_node = node
             if type(function_node) != type("a"):
                 """如果已经在函数节点内部 且 该函数节点不为空"""
                 class_Info = string[11:]
                 info_List = class_Info.split(' ')
                 class_node = graph.nodes.match("Class",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
                 if class_node is None:
                     """如果 函数内部所含的类节点还未在数据库中创建 则先在数据库中创建类节点"""
                     class_node = Node("Class",Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
                     graph.create(class_node)
                 """在数据库中创建 函数 与 包含类的 边"""
                 entity = Relationship(function_node, "includes class", class_node)
                 graph.create(entity)
             self.scan_class(string)
        else:
            self.location += 1 

    
    
     
       

    def scan_function(self, string):
        self.location = self.location + 1
        str_update = "Go"
        info = string[14:]
        info_List = info.split(' ')
        # 确认该函数节点是否建立，在neo库中进行搜索
        function_node = graph.nodes.match("Function",Path=info_List[0],Name=info_List[1],StartLine=info_List[3],EndLine=info_List[5]).first()
        if function_node is None:  # 若该函数在数据库中没有节点则创建新节点
            function_node = Node("Function", Path = info_List[0], Name = info_List[1], StartLine = info_List[3], EndLine = info_List[5])
        while ((str_update[0:13]!="EndFunction :") & (self.location < self.num_of_lines)):
            # str_input = get_line(self.filename, self.location)
            str_input =self.lines[self.location]
            str_update = str_input
            self.function_relation_scanner(str_input, function_node)
        self.location -= 1

    def scan_call(self, father_node):
        # function_Name = get_line(self.filename, self.location)
        #graph.create(Node("InCall"))
        """向下扫描一行 开始扫描"""
        self.location += 1
        """记录call 部分内部的初始位置"""
        start_position = self.location 
        name_list = []
        attr_list = []
        str_update = "Go"
        while((str_update[0:9]!="EndCall :") & (self.location < self.num_of_lines)):
            str_update = self.lines[self.location]
            """找到函数名 或者是类名或者包名"""
            if str_update[0:6]=="Name :":
               name_list.append(str_update)
            """找到类或者包的成员名"""
            if str_update[0:11]=="Attribute :":
               attr_list.append(str_update)
            """更新当前位置"""
            self.location += 1
        """从 while 中退出 则此时应该是 扫描到了EndCall"""
        end_postion =  self.location
        
        attr_count =len(attr_list)
        # graph.create(Node("Attr_Count",Count=attr_count))     
        #graph.create(Node("Attr_Count",attr_count))
        # graph.create(Node("Name_Count",name_list.count()))
        if attr_count==0:
            """无多级 则可能是类内部调用或者是 函数内部调用"""
            #graph.create(Node("进入"))
            function_name = name_list[0]
            function_path=function_name[7:]
            info_list = function_path.split(' ')
            """筛选出Function 函数所在文件路径 以及 名称都符合的"""
            function_node = graph.nodes.match("Function",Path=info_list[0],Name=info_list[1]).first()
            if function_node is not None:
                """如果有匹配的项，则进行连接"""
                graph.create(Relationship(father_node,"calls",function_node))
        elif attr_count==1:
            """这种情况可能是调用类的成员函数 或者是其他文件的函数"""
            test_name = name_list[0]
            test_path=test_name[7:]
            info_list = test_path.split(' ')
            attr_init=attr_list[0]
            attr_name=attr_init[12:]
            
            """首先测试是否调用的同文件下类的成员函数"""
            """同文件下类的 路径应与调用者路径相同"""
            class_node = graph.nodes.match("Class",Path=info_list[0],Name=info_list[1]).first()
            if class_node is not None:
                """找到所有与类节点有关系的节点"""
                # graph.create(Node("Class_node is not None"))
                function_nodes = find_linked_nodes(class_node)
                #graph.create(Node(str(len(function_nodes))))
                #graph.create(Node("Target",Path=info_list[0],Name=attr_name))
                for node in function_nodes:
                    """找到路径与 名称 都匹配的函数"""
                    if (node['Path']== info_list[0]) & (node['Name'] == attr_name):
                         graph.create(Relationship(father_node,"calls",node))
                         break
            else:
                """如果第一级不是类节点，那么则是文件节点"""
                file_nodes = graph.nodes.match("File")
                file_node = None
                for node in file_nodes:
                    """找到合适的文件节点"""
                    if node['Path'].find(info_list[1])!=-1:
                        file_node = node
                        break
                #graph.create(Node("Is Node"))
                if file_node is not None:
                    #graph.create(Node("Is not None"))
                    """如果文件节点不空"""
                    """找到所有与该文件节点有一层联系的节点,attr为1 则该被调用函数一定与第一层文件相连接"""
                    function_nodes = find_linked_nodes(file_node)
                    
                    for node in function_nodes:
                        """找到路径名称都相同的节点"""
                        if(node['Path']==file_node['Path'])&(node['Name']==attr_name):
                            graph.create(Relationship(father_node,"calls",node))
                            break
        else:
            """其它级 忽略"""
            if attr_count >= 3:
                return  
            """此时 的结构是 文件.类.函数"""
            file_line = name_list[0]
            file_info = file_line[7:]
            file_info_list=file_info.split(' ')
            file_nodes = graph.nodes.match("File")
            file_node = None
            for node in file_nodes:
                """找出合适的文件节点"""
                if node['Path'].find(file_info_list[1])!=-1:
                    file_node = node
                    break
            if file_node is not None:
                #graph.create(Node("File Node is not None"))
                """如果文件节点不空"""
                class_nodes=find_linked_nodes(file_node)
                class_node = None
                attr1=attr_list[0]
                attr2=attr_list[1]
                attr1=attr1[12:]
                attr2=attr2[12:]

                for node in class_nodes:
                    """找出合适的类节点"""
                    if (node['Path']==file_node['Path']) & (node['Name']==attr1):
                         class_node = node
                         break
                if class_node is not None:    
                   #graph.create(Node("Class Node is Not None"))
                   function_nodes=find_linked_nodes(class_node)
                   function_node=None
                   for node in function_nodes:
                      """找出最终的函数节点"""
                      #graph.create(Node("Function Node",Path=file_node['Path'],Name=attr2))
                      if(node['Path']==file_node['Path'])&(node['Name']==attr2):
                         function_node = node
                         """建立关系"""
                         graph.create(Relationship(father_node,"calls",function_node))
                         break

                
            
        # else:
        #     """有多级调用 则可能是 import的包 或者是 类"""
        #     name = name_list[0]
        #     class_node = graph.nodes.match("Class",Name=name)
        #     if class_node is None:
        #         """说明是文件中的元素"""

        #     else:
        #         """找到与类节点相连的所有节点"""                
        #         function_nodes_in_class = database_helper.find_linked_nodes(class_node)
        #         for node in function_nodes_in_class:
        #             if(node["Name"]==attr_list[1])
                

        



  
# graph_constructor('ast.txt',1)
# graph_constructor('ast.txt',2)