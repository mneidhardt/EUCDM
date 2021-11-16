from basestructures import BaseStructures
from graphs import Graph
from graphs import Node
import sys
import json

class EUCDMBuilder():
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
                json['type'] = "array"
                json['items'] = {}
                json['items']['type'] = jsontype
                # may be more here in relation to format, min/max etc...
                json['items']['description'] = str(node.getKey())
                json['maxItems'] = node.getCardinality()
                result[nodename] = json
            else:
                json['type'] = jsontype
                # may be more here in relation to format, min/max etc...
                json['description'] = str(node.getKey())
                result[nodename] = json
        else:
            json['properties'] = {}
            # json['properties']['kidCount'] = len(node.getChildren())
            result[nodename] = json
            for kid in node.getChildren():
                self.buildJSONSchema(kid, result[nodename]['properties'])
        
    def baseSchema(self):
        result = {}
        result['$schema'] = 'https://json-schema.org/draft/2019-09/schema'
        result['schemaVersion'] = '2.1.0'
        result['title'] = 'Declaration'
        result['type'] = 'object'
        result['additionalProperties'] = False
        result['properties'] = {}

        return result
        
        
    # Create JSON Schema out of the EUCDM, organised the right way.
    # First I build a graph from the file based EUCDM, and then I build a JSON Schema from the graph.
    def doJSONSchema(self, relfilename):
        bs = BaseStructures()
        relations = bs.getRelations(relfilename)

        mygraf = Graph(relations)
        root = Node('1', 1, 'Declaration', None)
        mygraf.buildGraph(root)
        # mygraf.showGraph(root)
        schema = {}
        self.buildJSONSchema(root, schema)              # Create the specific schema.
        result = self.baseSchema()                      # Create the base schema.
        result['properties'] = schema                   # Add specific to the base.
        result['properties']['schemaVersion'] = {}
        result['properties']['schemaVersion']['pattern'] = '^2[.][0-9]+[.][0-9]+$'
        result['properties']['schemaVersion']['type'] = 'string'
        result['properties']['procedureCategory'] = {}      # The current key for what EUCDM calls 'column'.
        result['properties']['procedureCategory']['type'] = 'string';
        result['properties']['procedureCategory']['maxLength'] = 3;
        #result['properties']['column']['type'] = 'string'
        #result['properties']['column']['enum'] = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'I1', 'I2']
        
        print(json.dumps(result))


relfilename = sys.argv[1] # Name of file containing relations.
builder = EUCDMBuilder()
builder.doJSONSchema(relfilename)

