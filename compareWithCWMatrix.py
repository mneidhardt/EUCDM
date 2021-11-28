import sys
from basestructures import BaseStructures

# This contains functions to extract column presence, i.e. a/b/c listed for each data element.
# I am investigating how to store them in a more normalised way.
#------------------------------------------------------------------------------

def extractColumnPresence(relations):
    columns = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'i1', 'i2']

    for row in relations:
        for i in range(5, len(row)):
            columnname = columns[i-5]
            if row[i] in ['a', 'b', 'c']:
                print(row[1], ';', columnname, ';', row[i])

if __name__ == "__main__":
    csvfilename = sys.argv[1] # Name of file containing CWs matrix.
    relfilename = sys.argv[2] # Name of file containing relations (the old way of serialising a graph).
    bs = BaseStructures()
    dedict = bs.getDEDict(csvfilename)
    relations = bs.getRelations(relfilename)
    for row in relations:
        if row[1] in dedict:
            formatmatch = dedict[row[1]][1] == row[4]
        else:
            formatmatch = row[1] + ' not in dedict!'
        print(row[1], row[2], row[3], row[4], formatmatch)

