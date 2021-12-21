from Graph import Graph

def CheckCPI(graph:Graph, errors:set = None):
    if errors == None: errors = set()
    for start in graph.nodes:
        edges = graph.GetEdgesFrom(start)
        for edge1 in edges:
            (start1, label1, end1, is_forward1) = edge1
            for edge2 in edges:
                (start2, label2, end2, is_forward2) = edge2
                for end in graph.nodes:

                    first = (end1, label2, end, is_forward2)
                    second = (end2, label1, end, is_forward1)

                    if graph.EdgeExists(first) and graph.EdgeExists(second) and graph.AreIndipendent(edge1, edge2):
                        
                        rev1 = graph.Reverse(edge1)
                        if not graph.AreIndipendent(rev1, first):
                            errors.add((rev1, first))
                        rev2 = graph.Reverse(edge2)
                        if not graph.AreIndipendent(rev2, second):
                            errors.add((rev2, second))
                        
    return len(errors)==0