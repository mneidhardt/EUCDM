import sys
import csv

# This will fix up the early versions of the relations table.
# E.g. add zeros to DENumbers, add DE names etc.
#-----------------------------------------------------------

def readDETable(filename):

def fixupData(filename, DETable):
    with open(filename) as csvfile:
        crdr = csv.reader(csvfile, delimiter=';')
        i = 0
        for row in crdr:
            if row[0].lstrip().startswith('#'):
                continue
            else:
                for i in range(0,3):
                    row[i] = int(row[i])
                for i in range(3,14):
                    row[i] = row[i].strip()
                relations.append(row)
    return relations
        
        
relfilename = sys.argv[1] # Name of file containing relations.
EUCDMFile = sys.argv[2]   # Name of file with the dump of CWs Excel sheet.
builder = EUCDMBuilder()
builder.doJSONSchema(relfilename)

