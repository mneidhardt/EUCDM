import json
import sys

# Node class for EUCDM Data Elements. Each such Data Element has a Data Element number,
# called DENumber or DENo. I store this in the field key.
# Cardinality is this node's cardinality in relation to its parent.
# Name is the textual name of the data element.
# Format is the type and size of the field, if any. E.g. an10 for 10 alphanumeric chars,
# and an..30 for 0-30 alphannumeric characters.
#----------------------------------------------------------------------------------------
class Node():
    def __init__(self, key, cardinality, name, format):
        self.key = key              # This is the full DENumber. String.
        self.cardinality = cardinality # Cardinality of this node in relation to its parent. Int.
        self.name = name                # Name of data element  String.
        self.format = format            # an..XY or similar, as in EUCDM. String.
        self.parent = None
        self.children = []
        
    def getKey(self):
        return self.key
     
    def getDENumber(self):
        return self.denumber

    def getParent(self):
        return self.parent

    def setParent(self, node):
        self.parent = node

    def getChildren(self):
        return self.children

    def addChild(self, node):
        self.children.append(node)

    def getCardinality(self):
        return self.cardinality

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getFormat(self):
        return self.format

    def setFormat(self, format):
        self.format = format

    def __repr__(self):
        result = []
        for v in [self.key, str(self.cardinality), self.name, self.format]:
            if v:
                result.append(v)

        return '; '.join(result)

class Graph():
    def __init__(self):
        self.count = 0
        self.schema = {}
        
    def showGraph(self, node, indent=''):
        print(indent, str(node))

        for kid in node.getChildren():
            self.showGraph(kid, indent+'    ')

    # Serialises a graph using end-of-child-markers.
    def serialiseGraph(self, root):
        result = []
        serialise(root, result)
        return result
    
    def serialise(self, node, result):
        result.append(node.getKey())
        if len(node.getChildren()) == 0:
            result.append('!')
            return
    
        for kid in node.getChildren():
            serialise(kid, result)
        result.append('!')
    
    # Deserialise a graph serialised using end-of-child-markers.
    def deserialiseGraph(self, nodes, cardinalities):
        idx = 0
        root = Node(nodes[idx], cardinalities[idx], None, None)
        self.deserialise(nodes, cardinalities, idx+1, root)
        return root
    
    def deserialise(self, nodes, cardinalities, idx, node):
        if idx >= len(nodes):
            return
        elif nodes[idx] == '!':
            self.deserialise(nodes, cardinalities, idx+1, node.getParent())
        else:
            child = Node(nodes[idx], cardinalities[idx], None, None)
            node.addChild(child)
            child.setParent(node)
            self.deserialise(nodes, cardinalities, idx+1, child)

