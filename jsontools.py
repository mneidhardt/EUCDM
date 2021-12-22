import json
import re
import datetime

class JSONTool():

    def __init__(self):
        self.pm = None

    def setPatternMatcher(self, patternmatcher):
        self.pm = patternmatcher

    #def toCamelCase(self, name):
    #    if name.strip() == '':
    #        return name
    #    if ' ' not in name:
    #        return name
    #    else:
    #        elements = name.split()
    #        result = elements.pop(0).lower()
    #        for e in elements:
    #            result += e.title()
    #        return result

    # I am not sure how to convert all the different names to camel case, consistently,
    # so for the time being, I do this.
    def convertName(self, name):
        return name.replace(' ', '_')

    def buildJSONSchema(self, node, result):
        nodename = self.convertName(node.getName())
        json = {}

        if node.getFormat():   # if there is a format, this is not an object.
            restrictions = self.pm.getRestrictions(node.getFormat())

            if node.getCardinality() > 1:
                json['description'] = str(node.getKey()) + '. EUCDM format=' + node.getFormat()
                json['type'] = 'array'
                json['maxItems'] = node.getCardinality()
                json['items'] = {}
                for r in restrictions:
                    json['items'][r[0]] = r[1]
                result[nodename] = json
            else:
                json['description'] = str(node.getKey()) + '. EUCDM format=' + node.getFormat()
                for r in restrictions:
                    json[r[0]] = r[1]
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
                    if 'required' not in json['items']:
                        json['items']['required'] = []
                    json['items']['required'].append(self.convertName(kid.getName()))
            else:
                json['description'] = str(node.getKey())
                json['type'] = 'object'
                json['additionalProperties'] = False
                json['properties'] = {}
                result[nodename] = json
                for kid in node.getChildren():
                    self.buildJSONSchema(kid, result[nodename]['properties'])
                    if 'required' not in json:
                        json['required'] = []
                    json['required'].append(self.convertName(kid.getName()))
        
    def buildJSONInstance(self, node):
        nodename = self.convertName(node.getName())

        if node.getFormat():   # if there is a format, this is not an object.
            # restrictions = self.parseFormat(node.getFormat())
            restrictions = self.pm.getRestrictions(node.getFormat())

            if node.getCardinality() > 1:
                json = []
                for i in range(0, min(node.getCardinality(), 2)):
                    json.append(self.pm.generateSample(node.getFormat()))
                return json
            else:
                # return '[' + node.getName() + '/' + node.getFormat() + ']'# TODO: return a realistic value following the format.
                return self.pm.generateSample(node.getFormat())
        else:
            if node.getCardinality() > 1:
                children = {}
                for kid in node.getChildren():
                    children[self.convertName(kid.getName())] = self.buildJSONInstance(kid)
                json = []
                json.append(children)
                return json
            else:
                json = {}
                for kid in node.getChildren():
                    childobj = self.buildJSONInstance(kid)
                    json[self.convertName(kid.getName())] = childobj
                return json
        
    def baseSchema(self, version):
        version = [str(e) for e in version] # Convert version numbers to strings.
        result = {}
        result['$schema'] = 'https://json-schema.org/draft/2019-09/schema'
        result['schemaVersion'] = '.'.join(version) # e.g. '2.1.0'
        result['title'] = 'Declaration'
        result['description'] = 'Created ' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
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
        
    def dumps(self, jsonstructure):
        return(json.dumps(jsonstructure))
