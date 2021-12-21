import json
import re
import datetime

class PatternMatcher():
    
    # Class for handling formats of the EUCDM.
    # They have several different formats:
    # Format       My interpretation, based on EU Law:
    # a2        => Alphabetic characters, exactly 2 of them.
    # a..2      => Alphabetic characters, 0 to 2 of them.
    # an2       => Alphanumeric characters, exactly 2 of them.
    # an..2     => Alphanumeric characters, 0 to 2 of them.
    # n4        => integer with 4 digits.
    # n4,5      => float with 4 digits, 2 of which are decimals.
    # n..4      => integer with 0 to 4 digits.
    # n..4,2    => float with 0 to 4 digits, 2 of which are decimals.
    #--------------------------------------------------------------------

    def __init__(self):
        self.patterns = []
        self.patterns.append(re.compile('^a(\d+)$', re.IGNORECASE))
        self.patterns.append(re.compile('^a\.\.(\d+)$', re.IGNORECASE))
        self.patterns.append(re.compile('^an(\d+)$', re.IGNORECASE))
        self.patterns.append(re.compile('^an\.\.(\d+)$', re.IGNORECASE))
        self.patterns.append(re.compile('^n(\d+)$'))
        self.patterns.append(re.compile('^n(\d+),(\d+)$'))
        self.patterns.append(re.compile('^n\.\.(\d+)$'))
        self.patterns.append(re.compile('^n\.\.(\d+),(\d+)$'))
        self.patterns.append(re.compile('^\s*$'))


    # Converts EUCDM format to restrictions used in JSON Schema.
    def getRestrictions(self, format):
        match = self.patterns[0].match(format)
        if match:
            minmax = '{' + match.group(1) + '}'
            return [['type', 'string'], ['pattern', '^[a-åA-Å]'+minmax+'$']]

        match = self.patterns[1].match(format)
        if match:
            minmax = '{0,' + match.group(1) + '}'
            return [['type', 'string'], ['pattern', '^[a-åA-Å]'+minmax+'$']]

        match = self.patterns[2].match(format)
        if match:
            minmax = '{' + match.group(1) + '}'
            return [['type', 'string'], ['pattern', '^[a-åA-Å0-9]'+minmax+'$']]

        match = self.patterns[3].match(format)
        if match:
            minmax = '{0,' + match.group(1) + '}'
            return [['type', 'string'], ['pattern', '^[a-åA-Å0-9]'+minmax+'$']]

        match = self.patterns[4].match(format)
        if match:
            max = int(pow(10, int(match.group(1)))-1)
            return [['type', 'integer'], ['minimum', 0], ['maximum', max]]

        match = self.patterns[5].match(format)
        if match:
            size1 = int(match.group(1)) # Size of the whole expression.
            size2 = int(match.group(2)) # Size of the decimals part.
            decimals = float(pow(10, -1*int(match.group(2))))
            max = float(pow(10, size1-size2)-1) + decimals
            return [['type', 'number'], ['minimum', max], ['maximum', max], ['multipleOf', decimals]]

        match = self.patterns[6].match(format)
        if match:
            max = int(pow(10, int(match.group(1)))-1)
            return [['type', 'integer'], ['minimum', 0], ['maximum', max]]

        match = self.patterns[7].match(format)
        if match:
            size1 = int(match.group(1)) # Size of the whole expression.
            size2 = int(match.group(2)) # Size of the decimals part.
            max = float(pow(10, size1-size2)-1)
            decimals = float(pow(10, -1*int(match.group(2))))
            return [['type', 'number'], ['minimum', 0], ['maximum', max], ['multipleOf', decimals]]

        match = self.patterns[8].match(format)
        if match:
            return []

        raise ValueError('Format "' + format + '" not understood.')
