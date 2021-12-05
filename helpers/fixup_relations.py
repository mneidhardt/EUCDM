import sys
import csv
from basestructures import BaseStructures

# This contains functions to manipulate the data, e.g. the relations file.
# One main aim is to be able to fix up the early versions of the relations table.
# E.g. add zeros to DENumbers, add DE names etc.
# Another aim is to be able to extract the 'column presence' and cardinality. This ought to be
# stored separately, and then joined when creating schemas.
#------------------------------------------------------------------------------

# Find duplicates in the relations file. 
def findDuplicates(relations):
    dict = {}
    
    for row in relations:
        key = row[0] + "/" + row[1]
        if key in dict:
            dict[key] += 1
            print("Duplicate: ", key)
        else:
            dict[key] = 1

# Read CSV file called filename. column = type of document, i.e. H1, H2, H3 etc.
def readDETable(filename):
    with open(filename) as csvfile:
        crdr = csv.reader(csvfile, delimiter=';')
        dedict = {}
        for row in crdr:
            if len(row) == 0:
                continue
            else:
                dedict[row[0]] = row
    return dedict

# Initially name and format was missing. This will look those 2 up
# in dedict, which is output from readDETable.
def addNameAndFormat(relations, dedict):
    newrelations = []
    
    for row in relations:
        if row[0] in dedict:
            row[3] = dedict[row[0]][2]
            row[4] = dedict[row[0]][3]
        if row[1] in dedict:
            row[3] = dedict[row[1]][2]
            row[4] = dedict[row[1]][3]

        newrelations.append(row)
    return newrelations

# Helper for recreateKeys.
def fixupKey(key):
    if len(key) == 4:
        tmp = [c for c in key]
        key = tmp[0]+tmp[1]+' '+tmp[2]+tmp[3]+' 000 000'
    elif len(key) == 7:
        tmp = [c for c in key]
        key = tmp[0]+tmp[1]+' '+tmp[2]+tmp[3]+' '+tmp[4]+tmp[5]+tmp[6]+' 000'

    return key

# Initially, I had thought to cast keys to integer, but I have
# changed my mind. So I recreate the keys as strings.
def recreateKeys(relations):
    newrelations = []
    
    for row in relations:
        row[0] = fixupKey(row[0])
        row[1] = fixupKey(row[1])
        newrelations.append(row)

    return newrelations

def addNewFields(relations):
    newrelations = []
    for row in relations:
        newrelations.append([row[0], row[1], row[2], '<DENAME>', '<FORMAT>'] + row[3:]) # Adding two fields to row.
    return newrelations

if __name__ == "__main__":
    relfilename = sys.argv[1] # Name of file containing relations.
    EUCDMFile = sys.argv[2]   # Name of file with the dump of CWs Excel sheet.
    bs = BaseStructures()
    relations = None    # This used to come from this method, but it's outdated: bs.getRelations(relfilename)
    # findDuplicates(relations) # Run this by itself, as it just prints out duplicates.
    relations = addNewFields(relations)
    relations = recreateKeys(relations)

    dedict = readDETable(EUCDMFile)
    relations = addNameAndFormat(relations, dedict)
    for row in relations:
        print(';'.join([str(e) for e in row]))
