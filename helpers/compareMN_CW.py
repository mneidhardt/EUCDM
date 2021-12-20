import sys
import os
sys.path.append(os.getcwd() + '/..')
from basestructures import BaseStructures
import csv


# I am comparing my values for CodeList with CWs list, which is a CSV version of his Excel sheet.
def compareMNandCW(file1, file2):
    bs = BaseStructures()
    dedict = bs.getDEDict(file2)

    with open(file1) as csvfile:
        crdr = csv.reader(csvfile, delimiter=';')
        i = 0
        for row in crdr:
            if row[0].strip().startswith('#'):
                continue
            else:
                if row[0] not in dedict:
                    print(row[0], 'not found in DEDict.')
                elif row[13].upper() != dedict[row[0]][2].upper():
                    print(row[0], ' not equal!')
                #print(row[0], row[13], dedict[row[0]][2], row[13].upper()==dedict[row[0]][2].upper())











if __name__ == "__main__":
    file1 = sys.argv[1] # Name of CSV file containing H7-data, made by MN.
    file2 = sys.argv[2] # Name of CSV file containing all EUCDM, made by CW.
    compareMNandCW(file1, file2)


