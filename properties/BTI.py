from Graph import Graph

def CheckBTI(graph:Graph, errors:set = None):
    if errors == None: errors = set()
    for node in graph.nodes:
        edges = graph.GetEdgesFrom(node, all=False, only_forward=False)
        for edge1 in edges:
            for edge2 in edges:
                if edge1 != edge2 and not graph.AreIndipendent(edge1, edge2):
                    errors.add((edge1, edge2))
    return len(errors)==0