import unittest
import sys
import os
sys.path.append(os.getcwd() + '/..')
from patternmatcher import PatternMatcher

class TestPatternMatcher(unittest.TestCase):
    def test_getRestrictions(self):
        pm = PatternMatcher()

        formats = ['a1', 'an18', 'a..3', 'an..512', 'n..12,5', 'n..16', 'n1', 'n2', 'n3', 'n12,2', '', '  ']
        results = [
                    [['type', 'string'], ['pattern', '^[a-åA-Å]{1}$']],
                    [['type', 'string'], ['pattern', '^[a-åA-Å0-9]{18}$']],
                    [['type', 'string'], ['pattern', '^[a-åA-Å]{0,3}$']],
                    [['type', 'string'], ['pattern', '^[a-åA-Å0-9]{0,512}$']],
                    [['type', 'number'], ['minimum', 0], ['maximum', 9999999.99999], ['multipleOf', 1e-05]],
                    [['type', 'integer'], ['minimum', 0], ['maximum', 9999999999999999]],
                    [['type', 'integer'], ['minimum', 0], ['maximum', 9]],
                    [['type', 'integer'], ['minimum', 0], ['maximum', 99]],
                    [['type', 'integer'], ['minimum', 0], ['maximum', 999]],
                    [['type', 'number'], ['minimum', 9999999999], ['maximum', 9999999999], ['multipleOf', 0.01]],
                    [],
                    []
                    ]

        for i in range(0, len(formats)):
            res = pm.getRestrictions(formats[i])
            self.assertEqual(results[i], res)

if __name__ == '__main__':
    unittest.main()
