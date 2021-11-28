from graphs import Node
import unittest

class TestNode(unittest.TestCase):
    def test_parseFormat(self):
        key = '12 01'
        cardinality = 9
        name = 'Nature of transaction'
        format = 'a6'
        node = Node(key, cardinality, name, format)
        node.addRestriction('type', 'string')
        node.addRestriction('pattern', '^[a-åA-Å]{6}$')
        node.addRestriction('minLength', '6')
        node.addRestriction('maxLength', '6')
        print(str(node))

        self.assertEqual(node.getKey(), key)
        self.assertEqual(node.getCardinality(), cardinality)
        self.assertEqual(node.getName(), name)
        self.assertEqual(node.getFormat(), format)

if __name__ == '__main__':
    unittest.main()
