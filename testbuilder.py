from graphs import Graph, Node

# Deserialising and serialising an N-ary graph.
# The serialising part is not really my focus here. I have added 4 '!'s at the end of the list of relations,
# so that it matches output from serialiser, though I think it's unnecessary, certainly in deserialisation.
#---------------------------------------------------------------------------------------------------
def getRelations():
    up = '↑' # Just for fun - made an up arrow with unicode - u2191.
    result = {}
    result['relations'] = ['1', '1212', '001', '!', '002', '!', '!', '7', '1212', '001', '!', '002', '!', '003', '!', '!', '!', '!']
    result['cardinalities'] = [1, 9, 1, 0, 1, 0, 0, 999, 9, 1, 0, 1, 0, 1, 0, 0]
    return result

def serialiseGraph(root):
    result = []
    serialise(root, result)
    return result

def serialise(node, result):
    result.append(node.getKey())
    if len(node.getChildren()) == 0:
        result.append('!')
        return

    for kid in node.getChildren():
        serialise(kid, result)
    result.append('!')

def deserialiseGraph(relations, cardinalities):
    idx = 0
    root = Node(relations[idx], cardinalities[idx], None, None)
    deserialise(relations, cardinalities, idx+1, root)
    return root

def deserialise(relations, cardinalities, idx, node):
    if idx >= len(relations):
        return
    elif relations[idx] == '!':
        deserialise(relations, cardinalities, idx+1, node.getParent())
    else:
        child = Node(relations[idx], cardinalities[idx], None, None)
        node.addChild(child)
        child.setParent(node)
        deserialise(relations, cardinalities, idx+1, child)

data = getRelations()
graf = deserialiseGraph(data['relations'], data['cardinalities'])

g = Graph(None)
g.showGraph(graf)

serialisation = serialiseGraph(graf)
# The 2 following lists should be the same:
print(serialisation)
print(data['relations'])
