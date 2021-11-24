import json

class JSONTool():
    def buildJSONSchema(self, node, result):
        nodename = node.getName().replace(' ', '_')
        json = {}

        if node.getFormat():   # if there is a format, this is not an object.
            if node.getFormat().startswith('a'):
                jsontype = 'string'
            elif node.getFormat().startswith('n'):
                jsontype = 'number'
            else:
                jsontype = None
                
            if node.getCardinality() > 1:
                json['description'] = str(node.getKey())
                json['type'] = "array"
                json['maxItems'] = node.getCardinality()
                json['items'] = {}
                json['items']['type'] = jsontype
                # may be more here in relation to format, min/max etc...
                result[nodename] = json
            else:
                json['description'] = str(node.getKey())
                json['type'] = jsontype
                # may be more here in relation to format, min/max etc...
                result[nodename] = json
        else:
            if node.getCardinality() > 1:
                json['description'] = str(node.getKey())
                json['type'] = 'array'
                json['maxItems'] = node.getCardinality()
                json['items'] = {}
                json['items'] = {}
                json['items']['type'] = 'object'
                json['items']['properties'] = {}
                result[nodename] = json
                for kid in node.getChildren():
                    self.buildJSONSchema(kid, result[nodename]['items']['properties'])
            else:
                json['description'] = str(node.getKey())
                json['type'] = 'object'
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
        
