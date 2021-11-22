from basestructures import BaseStructures
from graphs import Graph
from graphs import Node
import sys
import json

# Simulates returning serialised graph.
def getRelations():
    result = {}
    result['relations'] = ['1', '1212', '001', '!', '002', '!', '!', '7', '1212', '001', '!', '002', '!', '003', '!', '!']
    result['cardinalities'] = [1, 9, 1, 0, 1, 0, 0, 999, 9, 1, 0, 1, 0, 1, 0, 0]
    return result

def buildGraphRecursive(relations, cardinalities, idx, node):
    if idx >= len(relations):
        return node
    elif relations[idx] == '!':
        buildGraph(relations, cardinalities, idx+1, node.getParent())
    else:
        kid = Node(relations[idx], cardinalities[idx], None, None)
        if node is None:
            node = kid
        else:
            node.addChild(kid)
        buildGraph(relations, cardinalities, idx+1, kid)

def buildGraph(relations, cardinalities):
    node = Node(relations[0], cardinalities[0], None, None)

    for i in range(1, len(relations)):
        if relations[i] == '!':
            node = node.getParent()
        else:
            kid = Node(relations[i], cardinalities[i], None, None)
            kid.setParent(node)
            node = kid

    while True:
        if node.getParent() is not None:
            node = node.getParent()
        else:
            break

    graf = Graph(None)
    graf.showGraph(node)

result = getRelations()
graf = buildGraph(result['relations'], result['cardinalities'])



