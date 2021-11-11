from basestructures import BaseStructures
from graphs import Graph
from graphs import Node
import sys

class EUCDMBuilder():
    def showGraph(self, node, indent=''):
        print(indent, node.getKey()) # ,'(', node.getCardinality(), node.getType(), node.getFormat(), ')')

        if node.getType() == 'array':
            print(indent, '[')
        elif node.getType() == 'object':
            print(indent, '{')
            
        for kid in node.getChildren():
            self.showGraph(kid, indent+'    ')

        if node.getType() == 'array':
            print(indent, ']')
        elif node.getType() == 'object':
            print(indent, '}')

    def printList(self, filename):
        bs = BaseStructures()
        det = bs.constructDict(filename)
        list = bs.constructList(det)
        for k in list:
            print(k, ' = ', list[k])

    def printDETable(self, filename):
        bs = BaseStructures()
        det = bs.constructDict(filename)
        for k in det:
            print(k, ' > ', det[k])

    def doGrafWithSubgraphs(self, filename, relfilename):
        bs = BaseStructures()
        subgraphs = bs.constructDict2(filename, Node)        
        relations = bs.getRelations(relfilename)

        mygraf = Graph(relations)
        mygraf.setSubgraphs(subgraphs)
        root = Node(-1, None, 1, 'object', None)
        mygraf.buildGraph(root)
        self.showGraph(root)
        
    def doGraf(self, relfilename):
        bs = BaseStructures()
        relations = bs.getRelations(relfilename)

        mygraf = Graph(relations)
        root = Node(-1, None, 1, 'object', None)
        mygraf.buildGraph(root)
        self.showGraph(root)
        #bfslist = mygraf.bfs(root)
        #print(bfslist)
        
    def insertStatementsDE(self, dedict, delist):
        for r in delist:
            txt = dedict[r[4]][0]
            print("insert into dataelement (denum, denum1, denum2, denum3, denum4, key) values ('" + txt + "',", r[0],',', r[1],',', r[2],',', r[3],',',  r[4], ");");


filename = sys.argv[1]          # File containing the data elements (I use a dump of CW's Excel file).
relfilename = sys.argv[2] # Name of file containing relations.
builder = EUCDMBuilder()
# builder.doGrafWithSubgraphs(filename, relfilename)
builder.doGraf(relfilename)

