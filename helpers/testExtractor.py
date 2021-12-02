import sys
from basestructures import BaseStructures
from graphs import Graph

if __name__ == "__main__":
    filename = sys.argv[1] # Name of file containing relations.
    bs = BaseStructures()
    data = bs.readSerialisedGraph(filename)

    for row in data['nodes']:
        print(row)

    g = Graph()
    graf = g.deserialiseGraph(data['nodes'], data['cardinalities'])
    g.showGraph(graf)
