import sys
import datetime
import io
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

def syntax(legalcolumns):
    txt = []
    txt.append(sys.argv[0] + ' sg de cn')
    txt.append('  sg is the filename containing the serialied graph.')
    txt.append('  de is the filename containing the data elements, their names and formats.')
    txt.append('  cn is the columnname you want a schema for. Currently one of these:')
    txt.append(legalcolumns)
    return "\n".join(txt)

if __name__ == "__main__":

    try:
        legalcolumns = [ 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'I1', 'I2' ]

        filename = sys.argv[1] # Name of file containing serialised graph.
        defilename = sys.argv[2] # Name of file containing data element number, name and format.
        columnname = sys.argv[3] # 'Column' name, currently one of these:
        if columnname not in legalcolumns:
            raise ValueError()

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
            fh.write(jtool.dumps(result))

    except (IndexError, ValueError, NameError):
        print(syntax(','.join(legalcolumns)))
