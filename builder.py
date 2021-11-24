import sys
from graphs import Node

if __name__ == "__main__":
    filename = sys.argv[1] # Name of file containing serialised graph.
    bs = BaseStructures()
    nodelist = bs.getSerialisedGraph(filename)
    gtool = Graphs(None)
    graph = gtool.deserialiseGraph(nodelist)
    jtool = JSONTool()
    schema = {}
    root = Node('1', 1, 'Declaration', None)
    jtool.buildJSONSchema(root, schema)
    version = [2,2,0]
    result = jtool.baseSchema(version)
    result['properties'][root.getName()] = schema[root.getName()]
    print(json.dumps(result))

