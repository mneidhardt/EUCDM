import json
import sys
import re

# Node class for EUCDM Data Elements. Each such Data Element has a Data Element number,
# called DENumber or DENo.
# These data elements are organised in levels/groups like this:
# Top level, L1, has this form: 19 08 000 000
# Level 2, L2, has this form:   19 08 021 000
# Level 3, L3, has this form:   19 08 021 001
# I.e. the last two 3-digit groups can be either zero or non-zero.
# Each level therefore has a shorter key, with the DE number converted to integer, and 
# one or both zero groups discarded. I.e.:
# L1 has key of the form: zxyv
# L2 has key of the form: zxyvabc
# L3 has key of the form: zxyvabcdef
#--------------------------------------------------
class Node():
    def __init__(self, key, cardinality, name, format):
        self.key = key              # This is the full DENumber. String.
        self.cardinality = cardinality # Cardinality of this node in relation to its parent. Int.
        self.name = name                # Name of data element  String.
        self.format = format            # an..XY or similar, as in EUCDM. String.
        self.type = None                # JSON type. Will be set after construction.
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

    def getType(self):
        return self.type
        
    def setType(self, type):
        self.type = type

class Graph():
    def __init__(self, relations):
        self.count = 0
        self.schema = {}
        self.relations = relations    # The source list of relations that we convert to a tree graph.
        
    def showGraph(self, node, indent=''):
        print(indent, node.getKey(), '(', node.getCardinality(), node.getName(), node.getFormat(), ')')

        for kid in node.getChildren():
            self.showGraph(kid, indent+'    ')

    # The old way of constructing a graph. Not used any more.
    def buildGraph(self, parent):
        for row in self.relations:
            if row[0] == parent.getKey():
                kid = Node(row[1], row[2], row[3], row[4])
                parent.addChild(kid)
                self.buildGraph(kid)

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

