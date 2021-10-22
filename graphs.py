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
    def __init__(self, key, denumber, cardinality=0):
        self.key = key              # This is the DENumber as integer, and adapted to the level.
        self.denumber = denumber    # This is the full DE number, i.e. xx yy zzz æøå
        self.parent = None
        self.children = []
        self.cardinality = cardinality
        
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

    def setCardinality(self, value):
        self.cardinality = value

    def getCardinality(self):
        return self.cardinality

class Graph():
    def __init__(self, relations):
        self.count = 0
        self.relations = relations    # The source list of relations that we convert to a tree graph.
        self.subgraphs = {}         # Dict from basestructures, i.e. all L1 elements and their offspring.
        #self.detable = detable  # The table of Data Elements, with D.E.no, name etc.
        #self.dict2 = dict2      # A dict with all top elements as keys, and a graph of their subelements as value.
        #self.graph = Node()     # The resulting tree graph. Initially empty.
        #self.bs = bs            # An instance of BaseStructures.
        
    def setSubgraphs(self, subgraphs):
        self.subgraphs = subgraphs
        
    def buildGraph(self, parent):
        for row in self.relations:
            if row[0] == parent.getKey():
                kid = Node(row[1], None, row[2])
                parent.addChild(kid)
                if kid.getKey() in self.subgraphs:
                    kid.addChild(self.subgraphs[kid.getKey()])
                self.buildGraph(kid)
