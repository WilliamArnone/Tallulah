from Graph import Graph

def CheckIRE(graph:Graph, errors:set = None):
    if errors == None: errors = set()
    for indipendence in graph.indipendence:
        edge1, edge2 = indipendence
        event = graph.GetEventClass(edge1)
        for edge in event:
            if not graph.AreIndipendent(edge, edge2):
                errors.add((edge, edge2))
        event = graph.GetEventClass(edge2)
        for edge in event:
            if not graph.AreIndipendent(edge, edge1):
                errors.add((edge, edge1))
    return len(errors)==0