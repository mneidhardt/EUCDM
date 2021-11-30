import sys
import csv

# This is a function to read a CSV file containing (potentially) all Data Element numbers along with column presence info and cardinality.
# Specifically, the file has these columns:
# 1=Data element number
# 2-10: Each of the H and I columns.
# 11: Data element's cardinality in relation to Declaration level.
# 12: Data element's cardinality in relation to GS level.
# 13: Data element's cardinality in relation to SI level.
# 14: Codelist - either 'y', 'n' or empty.
# From this I build a serialised graph for the chosen 'column'.
# It's done by looping over the matrix once per cardinality column, thereby outputting the children of each level together.
# NB: It only produces a rough first edition of a serialised graph. 
# You must adjust the graph with more/less end-of-child markers, i.e. '!', because the function here doesnt handle sub and
# sub sub fields of data elements on the same level.
#--------------------------------------------------------------------------------------------------------------------------

def readFile(filename):
    data = []
    with open(filename) as csvfile:
        crdr = csv.reader(csvfile, delimiter=';')
        for row in crdr:
            if len(row) == 0 or row[0].lstrip().startswith('#'):
                continue
            else:
                data.append([x.strip() for x in row])
    return data

def extractSerialisedGraph(data, columnno):
    # columns: 'h1'=1, h2=2, h3=3, h4=4, h5=5, h6=6, h7=7, i1=8, i2=9.
    # cardcol: 10, 11 eller 12. Cardinality is in these columns, for D, GS and SI, respectively.
    indent = '    '
    for card in [10, 11, 12]:
        print(indent + 'Doing kids of level in column ' + str(card) + '. Remember to adjust sub- and subsubfields.')
        for row in data:
            if row[columnno] != '' and row[card] != '':
                cardinality = int(row[card])
                if cardinality == 1:
                    print(indent + row[0])
                else:
                    print(indent + row[0] + '/' + row[card])
                print('!')
        indent += '    '

if __name__ == "__main__":
    filename = sys.argv[1] # Name of file containing relations.
    data = readFile(filename)
    extractSerialisedGraph(data, 7)

