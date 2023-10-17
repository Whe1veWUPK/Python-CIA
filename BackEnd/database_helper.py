from py2neo import NodeMatcher, RelationshipMatcher

import ast_node_scanner

node_matcher = NodeMatcher(ast_node_scanner.graph)
relation_matcher = RelationshipMatcher(ast_node_scanner.graph)

"""获取与某节点有关系的所有节点（一层）"""
def find_linked_nodes(node):
    linked_nodes = set()
    matched_relations = relation_matcher.match(nodes=(None,node))
    linked_nodes.update([relation.start_node for relation in matched_relations])
    matched_relations = relation_matcher.match(nodes=(node,None))
    linked_nodes.update([relation.end_node for relation in matched_relations])
    return linked_nodes


test_node=ast_node_scanner.graph.nodes.match("Class",Name="test").first()
all_nodes=find_linked_nodes(test_node)
for node in all_nodes:
    print(node['Path'])
