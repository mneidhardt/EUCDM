import csv
import sys

#
# This class is meant to read input data, and process it into various structures that make it easier
# to construct a tree graph for the various columns (i.e. messages such as H1, H2 etc).
# From these graphs it should then be possible to create JSON or XML schemas.
#

class BaseStructures():

    # Return list of individual numers in DE number.
    # Expects a string as input, e.g. 12 01 000 000.
    # Returns a list of integers, e.g. [12, 1, 0, 0].
    def getDENumberSplitup(self, denumber):
        return [int(x) for x in denumber.split()]
    
    # Return the first 2 'digit groups' of the DENumber composed as 1 integer.
    # Expects a string as input, e.g. 12 01 000 000.
    # Returns an integer, e.g. 1201.
    def getPrefix1(self, denumber):
        denum = self.getDENumberSplitup(denumber)
        return denum[0]*100 + denum[1]
        
    # Return the first 3 'digit groups' of the DENumber composed as 1 integer.
    # Expects a string as input, e.g. 12 01 001 000.
    # Returns an integer, e.g. 1201001.
    def getPrefix2(self, denumber):
        denum = self.getDENumberSplitup(denumber)
        return denum[0]*100000 + denum[1]*1000 + denum[2]
        
    # Return all 'digit groups' of the DENumber composed as 1 integer.
    # Expects a string as input, e.g. 12 01 001 003.
    # Returns an integer, e.g. 1201001003.
    def getPrefix3(self, denumber):
        denum = self.getDENumberSplitup(denumber)
        return denum[0]*100000000 + denum[1]*1000000 + denum[2]*1000 + denum[3]
        
    def checkuniqueness(self, filename):
        with open(filename) as csvfile:
            crdr = csv.reader(csvfile, delimiter=';')
            h = {}
            for row in crdr:
                if len(row[59].strip()) > 0:
                    if row[0] in h:
                        h[row[0]] = h[row[0]] + 1
                    else:
                        h[row[0]] = 1
                        
            for key in h:
                if h[key] != 1:
                    print(key + ' ' + str(key))
                    
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
