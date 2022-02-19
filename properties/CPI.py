from Graph import EdgeToString, Graph, ReverseEdge

#t: P-α->Q and u: P-β->R and u': Q-β->S and t': R-α->S with t ι u  => u' ι nt
class CPI:

    name = "CPI - Coinitial Propagation of Indipendence"

    def Check(graph:Graph):
        """Check CPI property and return true if holds"""
        errors = set()

        #if an error is found we save the edges to complete the diamond
        indipendence_to_add = []
        keep_search = True
        while keep_search:

            keep_search = False
            #node is the P of the definition
            for start in graph.nodes:
                edges = graph.GetEdgesFrom(start)

                #edge1 is the t of the definition
                while len(edges)>0:
                    edge1 = edges.pop()
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
                            if graph.EdgeExists(first) and graph.EdgeExists(second) and (graph.AreIndependent(edge1, edge2)  or (edge1, edge2) in indipendence_to_add):
                                
                                #if there is not u' ι nt => we save those edges as errors
                                rev1 = ReverseEdge(edge1)
                                if not (graph.AreIndependent(rev1, first) or (rev1,first) in indipendence_to_add):
                                    indipendence_to_add.append((rev1, first))
                                    indipendence_to_add.append((first, rev1))
                                    errors.add((edge1, edge2, rev1, first))
                                    keep_search = True

                                rev2 = ReverseEdge(edge2)
                                if not (graph.AreIndependent(rev2, second) or (rev2,second) in indipendence_to_add):
                                    indipendence_to_add.append((rev2, second))
                                    indipendence_to_add.append((second, rev2))
                                    errors.add((edge1, edge2, rev2, second))
                                    keep_search = True

        #ordering errors, not fixable are on the top
        not_fixable = []
        fixable = []
        for error in errors:
            edge1, edge2, rev, edge = error
            if rev==edge: not_fixable.append(error)
            else: fixable.append(error)
        not_fixable.extend(fixable)
        
        return not_fixable
    
    def Apply(graph: Graph, error):
        """Remove CPI errors from the graph"""
        edge1, edge2, rev, edge = error
        if rev != edge: graph.AddIndipendence(rev, edge)

    def IsApplyable(error):
        """Returns True if the error can be fixed"""
        edge1, edge2, rev, edge = error
        return rev != edge

    def GetLog(error):
        """Returns the BTI errors in a (text, color) list"""
        log = []
        edge1, edge2, rev, edge = error
        if rev == edge:
            log.append((EdgeToString(edge1)+" ι "+EdgeToString(edge2), "green"))
            log.append(("would imply", "black"))
            log.append((EdgeToString(rev)+" ι "+EdgeToString(edge), "red"))
            log.append(("but this is", "black"))
            log.append(("not possible", "red"))
            log.append(("since independence is irreflexive", "black"))
        else:
            log.append((EdgeToString(edge1)+' ι '+EdgeToString(edge2), "green"))
            log.append(('but not', "black"))
            log.append((EdgeToString(rev)+" ι "+EdgeToString(edge), "red"))
        return log