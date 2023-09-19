from py2neo import Graph, Node, Relationship, NodeMatcher

'''
用于搜索ast_nodes.txt文件
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
    scan = my_scanner(num_of_lines, filename)
    my_scanner.scan_driver(scan)


def get_text_lines(filename):
    """给定文件路径，计算文件行数的函数"""
    count = len(open(filename, 'r').readlines())
    return count


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


class my_scanner:

    def __init__(self, num_of_lines, filename):

        self.num_of_lines = num_of_lines
        self.filename = filename
        self.location = 0

    def scan_driver(self):
        # 第一轮，搜索定义的函数建立节点
        while self.location < self.num_of_lines:
            string = get_line(self.filename, self.location)
            if string.find("FunctionDef") != -1:
                function_node_scanner(string)
            self.location = self.location + 1
        self.location = 0
        # 第二轮，建立边
        while self.location < self.num_of_lines:
            string = get_line(self.filename, self.location)
            self.function_relation_scanner(string, "Empty")

    def function_relation_scanner(self, string, node):
        if string.find("FunctionDef") != -1:
            self.scan_function(string)
        if string.find("Call") != -1:  # 发现函数之间的调用关系
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
        elif string.find("End") != -1:
            self.location = self.location + 1
            return None
        else:
            self.location = self.location + 1
            return None

    def scan_function(self, string):
        self.location = self.location + 1
        str_update = "Go"
        # 确认该函数节点是否建立，在neo库中进行搜索
        function_node = graph.nodes.match("Function").where("_.name=" + "'" + string[14:] + "'").first()
        if function_node is None:  # 若该函数在数据库中没有节点则创建新节点
            function_node = Node("Function", name=string[14:])
        while (str_update.find("EndFunction") == -1) & (self.location < self.num_of_lines):
            str_input = get_line(self.filename, self.location)
            str_update = str_input
            self.function_relation_scanner(str_input, function_node)
        # 由于已经到end行，回退一行
        self.location = self.location - 1

    def scan_call(self, node):
        function_Name = get_line(self.filename, self.location)
        while function_Name.find("Name :") == -1:
            self.location = self.location + 1
            function_Name = get_line(self.filename, self.location)
        if node == "Empty":
            return None
        # 确认该函数节点是否建立
        function_node = graph.nodes.match("Function").where("_.name=" + "'" + function_Name[7:] + "'").first()
        if function_node is not None:
            entity = Relationship(node, "calls", function_node)
            graph.create(entity)

