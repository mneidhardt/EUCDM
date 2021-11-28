import csv

#
# This class is meant to read input data, and process it into various structures that make it easier
# to construct a tree graph for the various columns (i.e. messages such as H1, H2 etc).
# From these graphs it is then possible to create JSON or XML schemas.
#

class BaseStructures():
    # Reads a serialised n-ary tree graph.
    # Returns a dict with 2 keys, 'nodes' and 'cardinalities'
    # The value for both keys are lists - of nodes and eoc-markerrs and cardinalities.
    # They are guaranteed to be of same length.
    #
    # Expects a serialisation using end-of-child-marker.
    # A serialised graph must have yne symbol/node per line, but a node can have a cardinality appended,
    # using a slash followed by an integer
    # As end-of-child marker I use exclamation mark. When one is encountered,
    # it means to go up one level.
    # As an example, the serialised graph (here you must imagine that commas are replaced with newlines ;):
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
                    raise ValueError('Something is not quite right on line ' + str(lineno))

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
