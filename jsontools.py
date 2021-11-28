import json
import re

class JSONTool():
    # Parse the format from EUCDM. They have several different ones:
    # pattern       My interpretation:
    # a2        => Alpha characters, exactly 2 of them.
    # a..2      => Alpha characters, 0 to 2 of them.
    # n4        => integer with 4 digits.
    # n..4      => integer with 1 to 4 digits (I'm unsure of this one).
    # n4,5      => float with 4 digits, 2 of which are decimals.
    # n..4,2    => float with 1 to 4 digits, 2 of which are decimals (I'm unsure of this one).
    def parseFormat(self, format):
        if format.strip() == '':
            return None

        p1 = re.compile('^a(\d+)$', re.IGNORECASE)
        p2 = re.compile('^a\.\.(\d+)$', re.IGNORECASE)
        p3 = re.compile('^an(\d+)$', re.IGNORECASE)
        p4 = re.compile('^an\.\.(\d+)$', re.IGNORECASE)
        p5 = re.compile('^n(\d+)$', re.IGNORECASE)
        p6 = re.compile('^n(\d+),(\d+)$', re.IGNORECASE)
        p7 = re.compile('^n\.\.(\d+)$', re.IGNORECASE)
        p8 = re.compile('^n\.\.(\d+),(\d+)$', re.IGNORECASE)

        match = p1.match(format)
        if match:
            minmax = '{' + match.group(1) + '}'
            return [['type', 'string'], ['pattern', '^[a-åA-Å]'+minmax+'$']]

        match = p2.match(format)
        if match:
            minmax = '{0,' + match.group(1) + '}'
            return [['type', 'string'], ['pattern', '^[a-åA-Å]'+minmax+'$']]

        match = p3.match(format)
        if match:
            minmax = '{' + match.group(1) + '}'
            return [['type', 'string'], ['pattern', '^[a-åA-Å0-9]'+minmax+'$']]

        match = p4.match(format)
        if match:
            minmax = '{0,' + match.group(1) + '}'
            return [['type', 'string'], ['pattern', '^[a-åA-Å0-9]'+minmax+'$']]

        match = p5.match(format)
        if match:
            max = str(pow(10, int(match.group(1)))-1)
            return [['type', 'integer'], ['minimum', '0'], ['maximum', max]]

        match = p6.match(format)
        if match:
            max = str(pow(10, int(match.group(1)))-1)
            decimals = str(pow(10, -1*int(match.group(2))))
            return [['type', 'number'], ['minimum', max], ['maximum', max], ['multipleOf', decimals]]

        match = p7.match(format)
        if match:
            max = str(pow(10, int(match.group(1)))-1)
            return [['type', 'integer'], ['minimum', '0'], ['maximum', max]]

        match = p8.match(format)
        if match:
            max = str(pow(10, int(match.group(1)))-1)
            decimals = str(pow(10, -1*int(match.group(2))))
            return [['type', 'number'], ['minimum', '0'], ['maximum', max], ['multipleOf', decimals]]

        raise ValueError('Format "' + format + '" not understood.')

    def buildJSONSchema(self, node, result):
        nodename = node.getName().replace(' ', '_')
        json = {}

        if node.getFormat():   # if there is a format, this is not an object.
            if node.getCardinality() > 1:
                json['description'] = str(node.getKey()) + '. EUCDM format=' + node.getFormat()
                json['type'] = 'array'
                json['maxItems'] = node.getCardinality()
                json['items'] = {}
                if node.getRestrictions():
                    restr = node.getRestrictions()
                    for k in restr:
                        json['items'][k] = restr[k]
                result[nodename] = json
            else:
                json['description'] = str(node.getKey()) + '. EUCDM format=' + node.getFormat()
                if node.getRestrictions():
                    restr = node.getRestrictions()
                    for k in restr:
                        json[k] = restr[k]
                result[nodename] = json
        else:
            if node.getCardinality() > 1:
                json['description'] = str(node.getKey())
                json['type'] = 'array'
                json['maxItems'] = node.getCardinality()
                json['items'] = {}
                json['items'] = {}
                json['items']['type'] = 'object'
                json['items']['additionalProperties'] = False
                json['items']['properties'] = {}
                result[nodename] = json
                for kid in node.getChildren():
                    self.buildJSONSchema(kid, result[nodename]['items']['properties'])
            else:
                json['description'] = str(node.getKey())
                json['type'] = 'object'
                json['additionalProperties'] = False
                json['properties'] = {}
                result[nodename] = json
                for kid in node.getChildren():
                    self.buildJSONSchema(kid, result[nodename]['properties'])
        
    def baseSchema(self, version):
        version = [str(e) for e in version] # Convert version numbers to strings.
        result = {}
        result['$schema'] = 'https://json-schema.org/draft/2019-09/schema'
        result['schemaVersion'] = '.'.join(version) # e.g. '2.1.0'
        result['title'] = 'Declaration'
        result['type'] = 'object'
        result['additionalProperties'] = False
        result['properties'] = {}
        result['properties']['schemaVersion'] = {}
        result['properties']['schemaVersion']['pattern'] = '^' + version[0] + '[.][0-9]+[.][0-9]+$'
        result['properties']['schemaVersion']['type'] = 'string'
        result['properties']['procedureCategory'] = {}      # The current key for what EUCDM calls 'column'. May be changed to 'column'.
        result['properties']['procedureCategory']['type'] = 'string';
        result['properties']['procedureCategory']['maxLength'] = 3;
        #result['properties']['column']['type'] = 'string'
        #result['properties']['column']['enum'] = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'I1', 'I2']

        return result
        
