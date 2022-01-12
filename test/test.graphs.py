import unittest
import sys
import os
import json
sys.path.append(os.getcwd() + '/..')
from graphs import Node, Graph
from patternmatcher import PatternMatcher

class TestGraph(unittest.TestCase):

    def test_BFS(self):
        g = Graph()

        nodes = '1,12,01,!,02,!,!,7,12,01,!,02,!,03'.split(',')
        cardinalities = '1,1,1,!,1,!,9,,1,1,!,1,!,1'.split(',')

        graf = g.deserialiseGraph(nodes, cardinalities)
        g.showGraph(graf)

        b = g.bfs(graf)
        for e in b:
            print(e)


if __name__ == '__main__':
    unittest.main()
