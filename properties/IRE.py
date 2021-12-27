from Graph import Graph

#t ∼ t' ι u => t ι u
def CheckIRE(graph:Graph, errors:set = None):
    """Check IRE property and return true if holds"""
    if errors == None: errors = set()
    #for each indipendent relation we want to check if also the edges of the same event are indipendent
    for indipendence in graph.indipendence:
        edge1, edge2 = indipendence
        event = graph.GetEventClass(edge1)
        for edge in event:
            if not graph.AreIndipendent(edge, edge2):
                errors.add((edge, edge2))
        #we must make 2 searches, one for edge1 and one for edge2
        event = graph.GetEventClass(edge2)
        for edge in event:
            if not graph.AreIndipendent(edge, edge1):
                errors.add((edge, edge1))
    return len(errors)==0