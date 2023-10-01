from py2neo import Graph, Node, Relationship, NodeMatcher

'''
用于搜索生成的节点信息文件
向neo4j中建立节点
包括函数节点，(包节点，类节点)
同时建立各个等级节点之间的调用情况
'''
num_of_function = 0
graph = Graph('bolt://localhost:7687', auth=('neo4j', '12345678'))
node_matcher = NodeMatcher(graph=graph)


# 调用该函数即可直接开始建立
def graph_constructor(filename):
    """向neo4j中构建图的函数"""
    num_of_lines = get_text_lines(filename)
    lines = get_lines(filename)
    scan = my_scanner(num_of_lines,lines,filename)
    my_scanner.scan_driver(scan)


def get_text_lines(filename):
    """给定文件路径，计算文件行数的函数"""
    count = len(open(filename, 'r').readlines())
    return count


def get_lines(filename):
    """给定文件路径，读取文件中所有行的函数"""
    f = open(filename,'r')
    line = f.readline()
    lines =[]
    while line:
        line = line.strip('\n')
        lines.append(line)
        line=f.readline()
    return lines

def get_line(filename, line_num):
    """给定文件路径以及行数，返回该行的数据"""
    with open(filename, 'r') as f:
        for num, line in enumerate(f):
            if num == line_num:
                return line


def function_node_scanner(string):
    # 给定函数节点名称，在图中查找该节点是否已经建立
    function_node = graph.nodes.match("Function").where("_.name=" + "'" + string[14:] + "'").first()
    if function_node is None:  # 若没有则创建新节点
        function_node = Node("Function", name=string[14:])
        graph.create(function_node)

def class_node_scanner(string):
    """给定类节点名称，在图中查找该节点是否已经建立"""
    class_node=graph.nodes.match("Class").where("_.name="+"'"+string[11:]+"'").first()
    if class_node is None: 
        """若没有则创建新节点"""
        class_node=Node("Class",name=string[11:])
        graph.create(class_node)

class my_scanner:

    def __init__(self, num_of_lines,lines,filename):

        self.num_of_lines = num_of_lines
        self.filename = filename
        self.lines=lines
        self.location = 0

    def scan_driver(self):
        
        """首先向数据库中建立 文件节点"""
        file_node = graph.nodes.match("File").where("_.name="+"'"+self.lines[self.location]+"'").first()
        if file_node is None:
           file_node=Node("File",name=self.lines[self.location])
           graph.create(file_node)
        self.location += 1
        """第一轮 建立节点(包括 函数 类)"""
        while self.location < self.num_of_lines:
            # string = get_line(self.filename, self.location)
            string = self.lines[self.location]
            if string.find("FunctionDef") != -1:
                function_node_scanner(string)
            elif string.find("ClassDef") != -1:
                class_node_scanner(string)
           
            self.location = self.location + 1

        self.location = 1
        # print("End First Round")
        """第二轮 建立节点之间的关系"""
        while self.location < self.num_of_lines:
            #string = get_line(self.filename, self.location)
            
            string = self.lines[self.location]
            """如果是文件结构的第一层，将包节点与第一层的所有节点进行连接"""
            """这里的连接 包括文件节点与 类节点 以及 函数节点之间的连接"""
            if string.find("FunctionDef") != -1:
                """建立文件节点与 第一层函数节点 之间的连接"""
                function_node = graph.nodes.match("Function").where("_.name="+"'"+string[14:]+"'").first()
                if function_node is None:
                    function_node = Node("Function",name=string[14:])
                    graph.create(function_node)
                entity = Relationship(file_node,"includes function",function_node)
                graph.create(entity)
                self.function_relation_scanner(string,"Empty")
            elif string.find("Call") != -1:
                self.function_relation_scanner(string,"Empty")
            elif string.find("ClassDef") != -1 :
                """建立文件节点 与 第一层类 节点之间的连接"""
                class_node = graph.nodes.match("Class").where("_.name="+"'"+string[11:]+"'").first()
                if class_node is None:
                    class_node = Node("Class",name = string[11:])
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
        """判断该类节点 是否有继承的父类"""
        if (father_class.find("Name") != -1) and (string.find("ClassDef")!=-1):
             """如果有继承的父类"""
             father_node = graph.nodes.match("Class").where("_.name="+"'"+father_class[7:]+"'").first()
             if father_node is None:
                 """如果 父类节点 还没有建立 则先在数据库中进行建立"""
                 father_node = Node("Class",name=father_class[7:])
                 graph.create(father_node)
             son_node = graph.nodes.match("Class").where("_.name="+"'"+string[11:]+"'").first()
             if son_node is None:
                 """如果 子类节点 还没有建立 则先在数据库中进行建立"""
                 son_node = Node("Class", name=string[11:])
                 graph.create(son_node)
             """建立子类 和 父类节点之间的关系"""
             entity = Relationship(father_node,"derives",son_node)
             graph.create(entity)

        if string.find("ClassDef") != -1:
            if type(node) != type("a"):
                """如果当前已经是在一个类节点内了 则需要对类和类进行连接"""
                """这里的判断意思是 初始node的类型是一个 string 如果被赋予了Node 类型 则表示已经在一个类的节点内部了"""
                class_node = graph.nodes.match("Class").where("_.name="+"'"+string[11:]+"'").first()
                if class_node is None :
                     """节点为空 则在neo4j 数据库中进行创建"""
                     class_node = Node("Class", name=string[11:])
                     graph.create(class_node)
                """连接 两个类节点"""
                entity = Relationship(node, "includes class", class_node)
                graph.create(entity)   
            self.scan_class(string)
            
        elif string.find("FunctionDef") != -1:
              if type(node) != type ("a") :
                  """如果当前已经是在一个类节点内 则需要对类和函数进行连接"""
                  """判断意思同上"""
                  class_node = node
                  function_node = graph.nodes.match("Function").where("_.name="+"'"+string[14:]+"'").first()
                  if function_node is None :
                      """函数节点不存在则进行创建"""
                      function_node = Node("Function", name = string[14:])
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
        class_node = graph.nodes.match("Class").where("_.name="+"'"+string[11:]+"'").first()
        if class_node is None :
            class_node = Node("Class", string[11:])
            graph.create(class_node)
        while((str_update.find("EndClass")==-1) and (self.location < self.num_of_lines)) :
            # str_input = get_line(self.filename, self.location)
            str_input = self.lines[self.location]
            str_update = str_input
            self.class_relation_scanner(str_input, class_node)
        
        self.location -= 1


        
        


    def function_relation_scanner(self, string, node):
        if string.find("FunctionDef") != -1:
            self.scan_function(string)
            
        elif string.find("Call") != -1:  # 发现函数之间的调用关系
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
        elif string.find("ClassDef") != -1:
             function_node = node
             if function_node != None:
                 """如果已经在函数节点内部 且 该函数节点不为空"""
                 class_node = graph.nodes.match("Class").where("_.name="+"'"+string[11:]+"'").first()
                 if class_node is None:
                     """如果 函数内部所含的类节点还未在数据库中创建 则先在数据库中创建类节点"""
                     class_node = Node("Class",name = string[11:])
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
        # 确认该函数节点是否建立，在neo库中进行搜索
        function_node = graph.nodes.match("Function").where("_.name=" + "'" + string[14:] + "'").first()
        if function_node is None:  # 若该函数在数据库中没有节点则创建新节点
            function_node = Node("Function", name=string[14:])
        while (str_update.find("EndFunction") == -1) & (self.location < self.num_of_lines):
            # str_input = get_line(self.filename, self.location)
            str_input =self.lines[self.location]
            str_update = str_input
            self.function_relation_scanner(str_input, function_node)
        self.location -= 1

    def scan_call(self, node):
        # function_Name = get_line(self.filename, self.location)
        function_Name =self.lines[self.location]
        while function_Name.find("Name :") == -1:
            self.location = self.location + 1
            # function_Name = get_line(self.filename, self.location)
            function_Name = self.lines[self.location]
        if node == "Empty":
            return None
        """确认该函数节点 是否建立"""
        function_node = graph.nodes.match("Function").where("_.name=" + "'" + function_Name[7:] + "'").first()
        if function_node is None and function_Name[7:]!="self":
              """如果所调用的函数节点为空 且不为类内部调用"""

              return None
        elif function_node is None and function_Name[7:]=="self":
              """如果所调用的函数节点为空 且是类内部调用"""

              function_Name = self.lines[self.location + 2]
              function_node = graph.nodes.match("Function").where("_.name="+"'"+function_Name[7:]+"'").first()
              entity = Relationship(node, "calls", function_node)
              graph.create(entity)
        elif function_node is not None and function_Name[7:]=="self":
              """如果所调用的函数节点不为空 且名称就是self """
              """则需进一步判断其是否是类的内部调用"""

              temp_Index = self.location + 2
              if temp_Index > self.num_of_lines:
                  """如果越界 则说明一定是 名称为 self 的 function"""
                  """建立关系后 返回"""
                  entity = Relationship(node, "calls", function_node)
                  graph.create(entity)
                  return None
              function_Name = self.lines[self.location + 2]
              if function_Name[0:9]=="Attribute":
                  """如果是类内部调用"""
                  function_node = graph.nodes.match("Function").where("_.name="+"'"+function_Name[12:]+"'").first()
                  entity = Relationship(node, "calls", function_node)
                  graph.create(entity)                             
              else:
                  """如果不是类内部调用"""
                  entity = Relationship(node, "calls", function_node)
                  graph.create(entity)                            

        elif function_node is not None and function_Name[7:]!="self":
              """如果所调用的函数节点不为空 且名称中不是 self"""
              """直接创建节点即可"""

              entity = Relationship(node, "calls", function_node)
              graph.create(entity)



  
