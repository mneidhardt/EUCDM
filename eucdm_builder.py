from basestructures import BaseStructures
from graphs import Graph
from graphs import Node
import sys
import json

class EUCDMBuilder():
    def showJSON(self, node, result):
        nodename = 'NAME' + str(node.getKey())
        json = {}

        if node.getFormat():   # if there is a format, this is not an object.
            if node.getCardinality() > 1:
                json['type'] = "array"
                json['items'] = {}
                json['items']['type'] = node.getFormat()
                json['items']['description'] = str(node.getKey()) + 'Name+DENo.'
                json['maxItems'] = node.getCardinality()
                result[nodename] = json
            else:
                json['type'] = node.getFormat()
                json['description'] = str(node.getKey()) + 'Name+DENo.'
                # may be more here in relation to format, min/max etc...
                result[nodename] = json
        else:
            json['properties'] = {}
            json['properties']['kidCount'] = len(node.getChildren())
            result[nodename] = json
            for kid in node.getChildren():
                self.showJSON(kid, result[nodename]['properties'])

    def showJSON_v1(self, node, result):
        nodename = '"NAME_' + str(node.getKey()) + '"'
        if node.getFormat():   # if there is a format, this is not an object.
            print(nodename + ': {')
            if node.getCardinality() > 1:
                print('"type" : "array",')
                print('"items": { "type": "xxx", "description":"blabla" }')
            else:
                print('"type": "', node.getFormat(), '",') 
                print('"description": "blabla"') 
                # may be more here in relation to format, min/max etc...
            print('},')
        else:
            print(nodename + ': {')
            print('"properties": {')
            print('"Kidcount": "', len(node.getChildren()), '",')
            for kid in node.getChildren():
                self.showJSON_v1(kid, result)
            print('    }')
            print('},')

    def showGraph(self, node, indent=''):
        print(indent, node.getKey(), '(', node.getCardinality(), node.getType(), node.getFormat(), ')')

        for kid in node.getChildren():
            self.showGraph(kid, indent+'    ')

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
        # self.showGraph(root)
        result = {}
        self.showJSON(root, result)
        print(json.dumps(result))
        
    def insertStatementsDE(self, dedict, delist):
        for r in delist:
            txt = dedict[r[4]][0]
            print("insert into dataelement (denum, denum1, denum2, denum3, denum4, key) values ('" + txt + "',", r[0],',', r[1],',', r[2],',', r[3],',',  r[4], ");");


filename = sys.argv[1]          # File containing the data elements (I use a dump of CW's Excel file).
relfilename = sys.argv[2] # Name of file containing relations.
builder = EUCDMBuilder()
# builder.doGrafWithSubgraphs(filename, relfilename)
builder.doGraf(relfilename)

