import sys
import csv

# This contains functions to extract column presence, i.e. a/b/c listed for each data element.
# I am investigating how to store them in a more normalised way.
#------------------------------------------------------------------------------

def extractColumnPresence(filename):
    with open(filename) as f:
        crdr = csv.reader(f, delimiter=';')
        for line in crdr:
            if line[0].lstrip().startswith('#'):
                headers = line
            else:
                for i in range(1,10):
                    if line[i].strip() != '':
                        print(line[0], ';', headers[i], ';', line[i])

def extractLevelCardinality(filename):
    with open(filename) as f:
        crdr = csv.reader(f, delimiter=';')
        for line in crdr:
            if line[0].lstrip().startswith('#'):
                headers = line
            else:
                for i in range(10,13):
                    if line[i].strip() != '':
                        print(line[0], ';', headers[i], ';', line[i])


if __name__ == "__main__":
    filename = sys.argv[1] # Name of CSV file containing base data, i.e. DEno, columns and cardinality.
    if sys.argv[2] == 'cp':
        extractColumnPresence(filename)
    elif sys.argv[2] == 'lc':
        extractLevelCardinality(filename)

