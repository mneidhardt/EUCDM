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
        self.type = None                # JSON type. Will be set after construction.
        self.restrictions = {}          # This contains restrictions on the type, e.g. minLength etc.
                                        # Key is e.g. minLength, value is e.g. 1, etc etc.
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

    def getRestrictions(self):
        return self.restrictions
        
    def addRestriction(self, key, value):
        self.restrictions[key] = value

    def __repr__(self):
        restr = []
        if len(self.restrictions) == 0:
            restr.append('')
        else:
            for k in self.restrictions:
                restr.append(k + ':' + self.restrictions[k])
        result = []
        for v in [self.key, str(self.cardinality), self.name, self.format, self.type]:
            if v:
                result.append(v)
        result.append('>>'.join(restr))
        return '; '.join(result)

class Graph():
    def __init__(self, relations):
        self.count = 0
        self.schema = {}
        self.relations = relations    # The source list of relations that we convert to a tree graph.
        
    def showGraph(self, node, indent=''):
        print(indent, str(node))

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

