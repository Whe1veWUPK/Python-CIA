import sys
import ast
import astunparse as astunparse
import astpretty

"""
通过AST提取需要信息
写入到ast_nodes.txt文件中
"""
def ast_constructor(filename):
    f = open(filename,encoding='utf-8')
    print(filename)
    ast_obj = ast.parse(f.read(),mode="exec")
    f.close()

    return ast_obj


class my_visitor(ast.NodeVisitor):
    def __init__(self,filepath):
        self.filepath = filepath

    def generic_visit(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        print("ClassDef : "+self.filepath+" "+node.name+" StartLine: "+str(node.lineno) + " EndLine: "+str(node.end_lineno))
        ast.NodeVisitor.generic_visit(self, node)
        print("EndClass :")

    def visit_AsyncFunctionDef(self, node):
        print("AsyncFunctionDef :", node.name)
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Call(self, node):
        print("Call :")
        ast.NodeVisitor.generic_visit(self, node)
        print("EndCall :")

    def visit_Import(self, node):
        print("Import :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_ImportFrom(self, node):
        print("ImportFrom :", node.module)
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_FunctionDef(self, node):
        print("FunctionDef : "+self.filepath+" "+node.name+" StartLine: "+str(node.lineno) + " EndLine: " + str(node.end_lineno))
        ast.NodeVisitor.generic_visit(self, node)
        print("EndFunction :")

    def visit_Name(self, node):
        print('Name : '+self.filepath+" "+node.id+" StartLine: " + str(node.lineno) + " EndLine: " + str(node.end_lineno))

    def visit_Constant(self, node):
        print("Constant :", node.value)

    def visit_JoinedStr(self, node):
        print("JoinedStr :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_List(self, node):
        print("List : elts")
        ast.NodeVisitor.generic_visit(self, node)

    #         #print("End :")

    def visit_Tuple(self, node):
        print("Tuple : elts")
        ast.NodeVisitor.generic_visit(self, node)

    #         #print("End :")

    def visit_Set(self, node):
        print("Set : elts")
        ast.NodeVisitor.generic_visit(self, node)

    #         #print("End :")

    def visit_Dict(self, node):
        print("Dict : keys, values")
        ast.NodeVisitor.generic_visit(self, node)

    #         #print("End :")

    def visit_Load(self, node):
        print("Load :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Store(self, node):
        print("Store :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Del(self, node):
        print("Del :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Starred(self, node):
        print("Starred :")
        ast.NodeVisitor.generic_visit(self, node)

    #         #print("End :")
    def visit_Attribute(self, node):
        print("Attribute : ")
        ast.NodeVisitor.generic_visit(self, node)
        print("attr : ", node.attr)

    def visit_Num(self, node):
        print('Num :', node.__dict__['n'])

    def visit_Str(self, node):
        print("Str :", node.s)

    def visit_alias(self, node):
        print("Alias :", node.name)

    def visit_Assign(self, node):
        print("Assign :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):
        print("Expr :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_FormattedValue(self, node):
        print("Formattedvalue: ", node.value, node.conversion, node.format_spec)

    def visit_UnaryOp(self, node):
        print("UnaryOp :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_UAdd(self, node):
        print("UAdd :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_USub(self, node):
        print("USub :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Not(self, node):
        print("Not :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Invert(self, node):
        print("Invert :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_BinOp(self, node):
        print("BinOp :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Add(self, node):
        print("Add :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Sub(self, node):
        print("Sub :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Mult(self, node):
        print("Mult :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Div(self, node):
        print("Div :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_FloorDiv(self, node):
        print("FloorDiv :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Mod(self, node):
        print("Mod :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Pow(self, node):
        print("Pow :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_LShift(self, node):
        print("LShift :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_RShift(self, node):
        print("RShift :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_BitOr(self, node):
        print("BitOr :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_BitXor(self, node):
        print("BitXor :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_BitAnd(self, node):
        print("BitAnd :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_MatMult(self, node):
        print("MatMult :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_BoolOp(self, node):
        print("BoolOp :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_And(self, node):
        print("And :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Or(self, node):
        print("Or :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Compare(self, node):
        print("Compare :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Eq(self, node):
        print("Eq :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_NotEq(self, node):
        print("NotEq :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Lt(self, node):
        print("Lt :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_LtE(self, node):
        print("LtE :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Gt(self, node):
        print("Gt :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_GtE(self, node):
        print("GtE :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Is(self, node):
        print("Is :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_IsNot(self, node):
        print("IsNot :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_In(self, node):
        print("In :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_NotIn(self, node):
        print("NotIn :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_keyword(self, node):
        print("keyword :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_IfExp(self, node):
        print("IfExp :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Attribute(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        print("Attribute :", node.attr)

    def visit_NamedExpr(self, node):
        print("NamedExpr :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Subscript(self, node):
        print("Subscript :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Slice(self, node):
        print("Slice :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_ListComp(self, node):
        print("ListComp :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_SetComp(self, node):
        print("SetComp :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_GeneratorExp(self, node):
        print("GeneratorExp :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_DictComp(self, node):
        print("DictComp :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_comprehension(self, node):
        print("comprehension :", node.ifs, node.is_async)
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_AnnAssign(self, node):
        print("AnnAssign :", node.simple)
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_AugAssign(self, node):
        print("AugAssign :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Raise(self, node):
        print("Raise :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Assert(self, node):
        print("Assert :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Delete(self, node):
        print("Delete :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Pass(self, node):
        print("Pass :")

    def visit_If(self, node):
        print("If :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_For(self, node):
        print("For :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_While(self, node):
        print("While :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Break(self, node):
        print("Break :")

    def visit_Continue(self, node):
        print("Continue :")

    def visit_Try(self, node):
        print("Try :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_ExceptHandler(self, node):
        print("ExceptHandler :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_With(self, node):
        print("With :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_withitem(self, node):
        print("withitem :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Lambda(self, node):
        print("Lambda :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_arguments(self, node):
        print("arguments :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_arg(self, node):
        print("arg :", node.arg)

    def visit_Return(self, node):
        print("Return :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Yield(self, node):
        print("Yield :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_YieldFrom(self, node):
        print("YieldFrom :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_Global(self, node):
        print("Global :")
        print(node.names)

    def visit_Nonlocal(self, node):
        print("Nonlocal :")
        print(node.names)

    def visit_Await(self, node):
        print("Await :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_AsyncFor(self, node):
        print("AsyncFor :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")

    def visit_AsyncWith(self, node):
        print("AsyncWith :")
        ast.NodeVisitor.generic_visit(self, node)
        # print("End :")
# f=open("ast.txt",'w')
# path=r'd:\PythonProjects\Python-CIA\test.py'
# sys.stdout=f
# tree = ast_constructor(path)

# visit = my_visitor(path)
# visit.visit(tree)
# tree = ast_constructor(r'test.py')
# # path = sys.path[0]+r'\BackEnd\ast_nodes.txt'
# # sys.stdout = open(path, 'w')
# visit = my_visitor(r'test.py')
# visit.visit(tree)
# tree = ast_constructor(r'test.py')

# sys.stdout=open(r'D:\PythonProjects\Python-CIA\output.txt','w')