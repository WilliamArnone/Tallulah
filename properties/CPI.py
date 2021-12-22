from Graph import Graph

#t: P-α->Q and u: P-β->R and u': Q-β->S and t': R-α->S with t ι u  => u' ι nt
def CheckCPI(graph:Graph, errors:set = None):
    if errors == None: errors = set()
    #node is the P of the definition
    for start in graph.nodes:
        edges = graph.GetEdgesFrom(start)

        #edge1 is the t of the definition
        for edge1 in edges:
            (start1, label1, end1, is_forward1) = edge1

            #edge2 is the u of the definition
            for edge2 in edges:
                (start2, label2, end2, is_forward2) = edge2

                #end is the S of the definition
                for end in graph.nodes:
                    #first is u' of the definition
                    first = (end1, label2, end, is_forward2)
                    #second is the t' of the definition
                    second = (end2, label1, end, is_forward1)

                    #we know t and u exist, if t ι u and t' and u' exist => u' ι nt
                    if graph.EdgeExists(first) and graph.EdgeExists(second) and graph.AreIndipendent(edge1, edge2):
                        
                        #if there is not u' ι nt => we save those edges as errors
                        rev1 = graph.Reverse(edge1)
                        if not graph.AreIndipendent(rev1, first):
                            errors.add((rev1, first))
                        rev2 = graph.Reverse(edge2)
                        if not graph.AreIndipendent(rev2, second):
                            errors.add((rev2, second))
                        
    return len(errors)==0