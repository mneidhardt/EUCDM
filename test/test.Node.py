import unittest
import sys
import os
sys.path.append(os.getcwd() + '/..')
from graphs import Node

class TestNode(unittest.TestCase):
    def test_parseFormat(self):
        key = '12 01'
        cardinality = 9
        name = 'Nature of transaction'
        format = 'a6'
        node = Node(key, cardinality, name, format)
        print(str(node))

        self.assertEqual(node.getKey(), key)
        self.assertEqual(node.getCardinality(), cardinality)
        self.assertEqual(node.getName(), name)
        self.assertEqual(node.getFormat(), format)

if __name__ == '__main__':
    unittest.main()
