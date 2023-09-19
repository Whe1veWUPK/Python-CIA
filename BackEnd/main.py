import ast
import astunparse as astunparse
import neo4j
func_def =\
"""
[1,2,3]
"""
cm = compile(func_def, '<string>', 'exec') # file.read()
exec(cm)
r_node = ast.parse(func_def)
print(astunparse.dump(r_node))
