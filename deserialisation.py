from graphs import Graph, Node
import csv
import sys

# Deserialising and serialising an N-ary graph.
# The serialising part is not really my focus here. I have added 4 '!'s at the end of the list of nodes,
# so that it matches output from serialiser, though I think it's unnecessary, certainly in deserialisation.
#---------------------------------------------------------------------------------------------------
def getRelations():
    up = '↑' # Just for fun - made an up arrow with unicode - u2191.
    result = {}
    result['nodes'] = ['1', '1212', '001', '!', '002', '!', '!', '7', '1212', '001', '!', '002', '!', '003', '!', '!', '!', '!']
    result['cardinalities'] = [1, 9, 1, 0, 1, 0, 0, 999, 9, 1, 0, 1, 0, 1, 0, 0]
    return result

def readNodelist(filename):
    nodes = []
    cardinalities = []

    with open(filename) as f:
        lineno=0
        for line in f:
            lineno += 1
            if line.strip().startswith('#'):
                continue
            elems = line.strip().split('/')

            if len(elems) == 2:
                nodes.append(elems[0])
                cardinalities.append(elems[1])
            elif len(elems) == 1 and elems[0] == '!':
                nodes.append('!')
                cardinalities.append('0')
            elif len(elems) == 1:
                nodes.append(elems[0])
                cardinalities.append('1')
            else:
                print('Something is not quite right on line ', lineno)
                sys.exit(1)

    data = {}
    data['nodes'] = nodes
    data['cardinalities'] = cardinalities
    return data

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

def deserialiseGraph(nodes, cardinalities):
    idx = 0
    root = Node(nodes[idx], cardinalities[idx], None, None)
    deserialise(nodes, cardinalities, idx+1, root)
    return root

def deserialise(nodes, cardinalities, idx, node):
    if idx >= len(nodes):
        return
    elif nodes[idx] == '!':
        deserialise(nodes, cardinalities, idx+1, node.getParent())
    else:
        child = Node(nodes[idx], cardinalities[idx], None, None)
        node.addChild(child)
        child.setParent(node)
        deserialise(nodes, cardinalities, idx+1, child)


#data = readNodelist(filename)
#print(data['nodes'])
#print(data['cardinalities'])
#sys.exit(1)

filename = sys.argv[1]
data = readNodelist(filename)
graf = deserialiseGraph(data['nodes'], data['cardinalities'])

g = Graph(None)
g.showGraph(graf)

serialisation = serialiseGraph(graf)
# The 2 following lists should be the same:
print(serialisation)
print(data['nodes'])
