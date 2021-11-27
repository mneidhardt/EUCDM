import csv
import sys
import re

#
# This class is meant to read input data, and process it into various structures that make it easier
# to construct a tree graph for the various columns (i.e. messages such as H1, H2 etc).
# From these graphs it is then possible to create JSON or XML schemas.
#

class BaseStructures():

    def parseFormat(self, format):
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

    # Jeg er usikker på hvordan n12 skal forstås: maximum 12, eller max 12 cifre?

        raise ValueError('Format "' + format + '" not understood.')

    # Reads a serialised n-ary tree graph.
    # Expects a serialisation using end-of-child-marker.
    # As end-of-child marker I use exclamation mark. When one is encountered,
    # it means to go up one level.
    # Also, each can have a cardinality attached, by appending a slash and a number to the node.
    # and the serialised graph is written to file with one symbol per line.
    # As an example, the serialised graph:
    # 1,12,01,!,02,!,!,7/9,12,01,!,02,!,03
    # deserialises to this graph:
    #        1
    #       / \
    #    12    7
    #   / \     \
    # 01  02     12
    #          /  |  \
    #         01  02  03
    # The node labelled 7 has cardinality of 9, though this is not shown in the graph.
    # This is used in JSON Schema.
    #---------------------------------------------------------------------------------
    def readSerialisedGraph(self, filename):
        nodes = []
        cardinalities = []

        with open(filename) as f:
            lineno=0
            for line in f:
                lineno += 1
                line = line.strip()
                if line.startswith('#'):
                    continue
                elems = [e.strip() for e in line.split('/')]

                if len(elems) == 2:
                    nodes.append(elems[0])
                    cardinalities.append(int(elems[1]))
                elif len(elems) == 1 and elems[0] == '!':
                    nodes.append('!')
                    cardinalities.append(0)
                elif len(elems) == 1:
                    nodes.append(elems[0])
                    cardinalities.append(1)
                else:
                    print('Something is not quite right on line ', lineno)
                    sys.exit(1)

        data = {}
        data['nodes'] = nodes
        data['cardinalities'] = cardinalities
        return data

    # Reads a file with semicolon separated values and returns a dict with this:
    # Key = dataelement number (xx yy zzz vvv)
    # Value = [dataelement-name, format]
    def  getDEDict(self, filename):
        dict = {}
        with open(filename) as csvfile:
            crdr = csv.reader(csvfile, delimiter=';')
            for row in crdr:
                if len(row) == 0 or row[0].lstrip().startswith('#'):
                    continue
                else:
                    dict[row[0].strip()] = [row[2].strip(), row[3].strip()]
        return dict

    # Read CSV file called filename. column = type of document, i.e. H1, H2, H3 etc.
    def readit(self, filename, column):
        with open(filename) as csvfile:
            crdr = csv.reader(csvfile, delimiter=';')
            i = 0
            for row in crdr:
                if len(row[column].strip()) > 0:
                    print(';'.join(row[0:3]) + ';' + row[column] + ';' + ';'.join(row[62:69]))
                    i = i+1
            print(str(i) + ' rows.')

    # Old version - probably outdated now.
    # Reads CSV file with relations for toplevel DataElements.
    # Format is:
    # parent, child, cardinality, name, format, h1,h2,h3,h4,h5,h6,h7,i1,i2
    # The h1-h7,i1-i2 columns have 'a', 'b', 'c' or '-', meaning 'a'=mandatory, 'b'=optional, 'c'=optional for ms, '-'=N/A.
    def getRelations(self, filename):
        relations = []
        
        with open(filename) as csvfile:
            crdr = csv.reader(csvfile, delimiter=';')
            i = 0
            for row in crdr:
                if len(row) == 0 or row[0].lstrip().startswith('#'):
                    continue
                else:
                    for i in range(0,2):
                        row[i] = row[i].strip()
                    row[2] = int(row[2])
                    for i in range(3,len(row)):
                        row[i] = row[i].strip()
                    relations.append(row)
        return relations
