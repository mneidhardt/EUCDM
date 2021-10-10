import json
import sys
import re

class Node():
    def __init__(self):
        self.data = None
        self.parent = None
        self.children = []
     
    def getData(self):
        return self.data

    def setData(self, content):
        self.data = content

    def getParent(self):
        return self.parent

    def setParent(self, node):
        self.parent = node

    def getChildren(self):
        return self.children

    def addChild(self, node):
        self.children.append(node)

class Graph():
    def __init__(self, data, detable):
        self.count = 0
        self.data = data # The source list of relations that we convert to a tree graph.
        self.detable = detable  # The table of Data Elements, with D.E.no, name etc.
        self.graph = Node()  # The resulting tree graph. Initially empty.
        
    def buildGraph(self, parent):
        for row in self.data:
            if row[0] == parent.getData():
                kid = Node()
                kid.setData(row[1])
                parent.addChild(kid)
                self.buildGraph(kid)
                
    def showGraph(self, node, indent=''):
        id = node.getData()
        denumber = self.detable[id][0]
        dename = self.detable[id][2]
        print(indent, id, denumber)
        
        for kid in node.getChildren():
            self.showGraph(kid, indent+'  ')

    # This shows any graph constructed of Nodes, without using detable.
    def showGraph2(self, node, indent=''):
        print(indent, node.getData())
        
        for kid in node.getChildren():
            self.showGraph2(kid, indent+'  ')

    # This takes a list as made by BaseStructures.constructList,
    # and builds all the little graphs with root XX ZZ 000 000.
    def buildParts(self, delist):
        result = {}
        for x in range(1,100):
            continue # Will get back to this...
