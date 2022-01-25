from Graph import Graph

#t: P~α~>Q and t': P~β~>Q' and t=/=t'  =>  t ι t'
def CheckBTI(graph:Graph):
    """Check BTI property and return true if holds"""
    errors = set()

    #node is the P of the definition
    for node in graph.nodes:
        edges = graph.GetEdgesFrom(node, all=False, only_forward=False)

        #edge1 is the t of the definition
        for edge1 in edges:
            #edge2 is the u of the definition
            for edge2 in edges:
                #t and u are coinitial, so if they are not the same edge they must be indipendent
                if edge1 != edge2 and not graph.AreIndipendent(edge1, edge2):
                    errors.add((edge1, edge2))
    return errors