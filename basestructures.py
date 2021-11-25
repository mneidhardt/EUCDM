import csv
import sys

#
# This class is meant to read input data, and process it into various structures that make it easier
# to construct a tree graph for the various columns (i.e. messages such as H1, H2 etc).
# From these graphs it should then be possible to create JSON or XML schemas.
#

class BaseStructures():

    # Reads a serialised n-ary tree graph.
    # Expects a serialisation using end-of-child-marker.
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
