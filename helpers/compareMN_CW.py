import sys
import os
sys.path.append(os.getcwd() + '/..')
from basestructures import BaseStructures
import csv

# Read CSV file into a matrix and return it.
def readCSV(filename):
    matrix = []

    with open(filename) as csvfile:
        crdr = csv.reader(csvfile, delimiter=';')
        for row in crdr:
            if row[0].strip().startswith('#'):
                continue
            else:
                matrix.append(row)

    return matrix

def cleanup(matrix):
    result = []

    for row in matrix:
        if len(row) < 69:
            continue

        for i in range(62, 69):
            row[i] = row[i].lower().replace('x', '')
            result.append(row)
    return result

# Given 2 matrices, mat1 and mat2, compare mat1.col1 with mat2.col2.
# The premise is that mat1[0] and mat2[0] contain keys, i.e DENo, but mat1[0] contains only a subset
# of the keys in mat2[0].
def compareColumns(mat1, mat2, col1, col2):
    totalrows=0
    misses=0
    for r1 in mat1:
        totalrows += 1
        for r2 in mat2:
            if r1[0] == r2[0]:
                if r1[col1].upper() != r2[col2].upper():
                    misses += 1
                    print('   Mismatch.', r1[0] + ':', r1[col1] + ' != ' + r2[col2])
                break

    print(totalrows, misses)

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











if __name__ == "__main__":
    file1 = sys.argv[1] # Name of CSV file containing H7-data, made by MN.
    file2 = sys.argv[2] # Name of CSV file containing all EUCDM, made by CW.
    col1 = int(sys.argv[3])  # Number of the column in the first matrix to check.
    col2 = int(sys.argv[4])  # Number of the column in the second matrix to check.
    # compareMNandCW(file1, file2)
    mat1 = readCSV(file1)
    mat2 = readCSV(file2)
    mat2 = cleanup(mat2)
    compareColumns(mat1, mat2, col1, col2)


