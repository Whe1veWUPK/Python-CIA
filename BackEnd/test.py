import ast
import astpretty

def ast_constructor(filename):
    f = open(filename)
    print(filename)
    ast_obj = ast.parse(f.read(), mode="exec")
    print(astpretty.pprint(ast_obj))
    f.close()

    return ast_obj


ast_constructor(r'test.py')






