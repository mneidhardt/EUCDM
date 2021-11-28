import sys
import json
import datetime
import io
import re
from graphs import Node, Graph
from basestructures import BaseStructures
from jsontools import JSONTool

# This will add name, format and restrictions to nodes of a graph
# dedict contains, for each dataelement, it's name and format.
# The restrictions are created based on the format, and together 
# they make up the validation of the node. 
def annotateNodes(node, dedict, jt):
    # print(indent, node.getKey(), '(', node.getCardinality(), node.getName(), node.getFormat(), ')')
    node.setName(dedict[node.getKey()][0])
    node.setFormat(dedict[node.getKey()][1])
    restrictions = jt.parseFormat(node.getFormat())
    if restrictions:
        for r in restrictions:
            node.addRestriction(r[0], r[1])

    for kid in node.getChildren():
        annotateNodes(kid, dedict, jt)


if __name__ == "__main__":
    columnname = 'h1'

    filename = sys.argv[1] # Name of file containing serialised graph.
    defilename = sys.argv[2] # Name of file containing data element number, name and format.

    bs = BaseStructures()
    gtool = Graph()
    jtool = JSONTool()

    sgraf = bs.readSerialisedGraph(filename)
    dedict = bs.getDEDict(defilename)
    graf = gtool.deserialiseGraph(sgraf['nodes'], sgraf['cardinalities'])
    annotateNodes(graf, dedict, jtool)
    gtool.showGraph(graf)
    schema = {}
    jtool.buildJSONSchema(graf, schema)
    version = [2,2,0]
    result = jtool.baseSchema(version)
    result['properties'][graf.getName()] = schema[graf.getName()]

    schemafilename = columnname + '.schema.' + datetime.datetime.now().strftime("%Y-%m-%d") + '.json'
    with io.open(schemafilename, 'w', encoding='utf8') as fh:
        fh.write(json.dumps(result))

