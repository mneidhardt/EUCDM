from basestructures import BaseStructures
from graphs import Graph
from graphs import Node
import sys
import json

class BaseStructuresTest():
    def getRelationsTest(self, relfilename):
        bs = BaseStructures()
        relations = bs.getRelations(relfilename)

        print(len(relations))
        for row in relations:
            print(len(row))
            for e in row:
                print('>' + str(e) + '<', end='')
            print()

relfilename = sys.argv[1] # Name of file containing relations.
tester = BaseStructuresTest()
tester.getRelationsTest(relfilename)

