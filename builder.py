import sys
import json
import datetime
import io
from graphs import Node, Graph
from basestructures import BaseStructures
from jsontools import JSONTool

# This will add name and format to nodes of a graph
def annotateNodes(node, namedict):
    # print(indent, node.getKey(), '(', node.getCardinality(), node.getName(), node.getFormat(), ')')
    node.setName(namedict[node.getKey()][0])
    node.setFormat(namedict[node.getKey()][1])

    for kid in node.getChildren():
        annotateNodes(kid, namedict)


if __name__ == "__main__":
    columnname = 'h1'

    filename = sys.argv[1] # Name of file containing serialised graph.
    defilename = sys.argv[2] # Name of file containing data element number, name and format.
    bs = BaseStructures()
    sgraf = bs.readSerialisedGraph(filename)
    dedict = bs.getDEDict(defilename)
    gtool = Graph(None)
    graf = gtool.deserialiseGraph(sgraf['nodes'], sgraf['cardinalities'])
    annotateNodes(graf, dedict)
    gtool.showGraph(graf)
    jtool = JSONTool()
    schema = {}
    jtool.buildJSONSchema(graf, schema)
    version = [2,2,0]
    result = jtool.baseSchema(version)
    result['properties'][graf.getName()] = schema[graf.getName()]

    schemafilename = columnname + '.schema.' + datetime.datetime.now().strftime("%Y-%m-%d") + '.json'
    with io.open(schemafilename, 'w', encoding='utf8') as fh:
        fh.write(json.dumps(result))

