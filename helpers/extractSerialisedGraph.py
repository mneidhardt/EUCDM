import sys
import csv

# This is a script to read a CSV file containing (potentially) all Data Element numbers along with column presence info and cardinality.
# Specifically, the file has these columns:
# 1=Data element number
# 2-10: Each of the H and I "columns" (or any other group of "columns" that are coupled in te EUCDM).
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

# Function to determine action when receiving a DE, given the previous one.
#
def determineAction(previous, current):
    if previous == '':
        previous = '00 00 000 000'
    prevI = [int(x) for x in previous.split()]
    currI = [int(x) for x in current.split()]

    if previous[0:5] == current[0:5] and prevI[2] == 0 and prevI[3] == 0 and currI[2] > 0 and currI[3] == 0:
        return(['    ', None]) # Transition 2, State 1->2
    elif previous[0:5] != current[0:5] and currI[2] == 0 and currI[3] == 0 and prevI[2] > 0 and prevI[3] == 0:
        return(['', '!\n!'])    # Transition 3, State 2->1
    elif previous[0:5] == current[0:5] and prevI[2] > 0 and prevI[3] == 0 and currI[2] > 0 and currI[3] == 0:
        return(['    ', '!']) # Transition 4, State 2->2
    elif previous[0:9] == current[0:9] and prevI[3] == 0 and currI[3] > 0:
        return(['        ', None]) # Transition 5, State 2->3
    elif previous[0:9] == current[0:9] and prevI[3] > 0 and currI[3] == 0:
        return(['    ', '!']) # Transition 6, State 3->2
    elif previous[0:9] == current[0:9] and prevI[2] > 0 and prevI[3] > 0 and currI[2] > 0 and currI[3] > 0:
        return(['        ', '!']) # Transition 7, State 3->3
    elif previous[0:5] != current[0:5] and prevI[2] > 0 and prevI[3] > 0 and currI[2] == 0 and currI[3] == 0:
        return(['', '!\n!\n!'])  # Transition 8, State 3->1
    else:
        return(['', None])

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

# Get a rough form of the serialised graf by going through a matrix with this for each line:
# DENo;H1;h2;h3;h4;h5;h6;h7;h8;i1;i2;Card-D;Card-GS;Card-SI
# The columns right after DENo contain a, b, c or nothing, depending on whether field is present on respective 'column'.
# The remaining 3 columns contain the cardinality for the DE on the respective level.
# Args: Data is the matrix outlined above, possibly with more columns.
# columnno: the column in the matrix for which you want fields, e.g. 7 if you want H7-fields.
# cardcolumns: the columns in which to look for cardinalities. The function's outer loop loops over these.
#-----------------------------------------------------------------------------------------------------------------
def extractSerialisedGraph(data, columnno, cardcolumns):
    indent = '    '
    for card in cardcolumns:
        print(indent + 'Doing kids of level in column ' + str(card) + '. Remember to adjust sub- and subsubfields.')
        previous = ''
        for row in data:
            if row[columnno] != '' and row[card] != '':
                action = determineAction(previous, row[0])      # Determine what to output.
                if action[1] is not None:
                    print(action[1])

                cardinality = int(row[card])
                if cardinality == 1:
                    print(action[0] + row[0])      # 1 is default cardinality, so I dont print it.
                else:
                    print(action[0] + row[0] + '/' + row[card])

                previous = row[0]

if __name__ == "__main__":
    filename = sys.argv[1] # Name of file containing relations.
    columncol = 7;             # Which message are you after? H7 happens to be in column 7.
    cardcolumns = [10,11,12] # When reading my own little test matrix, DEColumnPresenceCardinality.csv
    data = readFile(filename)

    #previous = ''
    #for row in data:
    #    action = determineAction(previous, row[0])
    #    if action[1] is not None:
    #        print(action[1])
    #    print(action[0] + row[0])
    #    previous = row[0]

    extractSerialisedGraph(data, columncol, cardcolumns)

