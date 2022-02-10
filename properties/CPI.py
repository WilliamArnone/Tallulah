from Graph import EdgeToString, Graph, ReverseEdge

#t: P-α->Q and u: P-β->R and u': Q-β->S and t': R-α->S with t ι u  => u' ι nt
class CPI:
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
                            if graph.EdgeExists(first) and graph.EdgeExists(second) and (graph.AreIndipendent(edge1, edge2)  or (edge1, edge2) in indipendence_to_add):
                                
                                #if there is not u' ι nt => we save those edges as errors
                                rev1 = ReverseEdge(edge1)
                                if not (graph.AreIndipendent(rev1, first) or (rev1,first) in indipendence_to_add):
                                    indipendence_to_add.append((rev1, first))
                                    indipendence_to_add.append((first, rev1))
                                    errors.add((edge1, edge2, rev1, first))
                                    keep_search = True

                                rev2 = ReverseEdge(edge2)
                                if not (graph.AreIndipendent(rev2, second) or (rev2,second) in indipendence_to_add):
                                    indipendence_to_add.append((rev2, second))
                                    indipendence_to_add.append((second, rev2))
                                    errors.add((edge1, edge2, rev2, second))
                                    keep_search = True
                            
        return errors
    
    def Apply(graph: Graph, errors):
        """Remove CPI errors from the graph"""
        for error in errors:
            edge1, edge2, rev, edge = error
            if rev != edge: graph.AddIndipendence(rev, edge)

    def ToString(errors):
        """Returns the CPI errors in a string"""

        log = [('CPI - Coinitial Propagation of Indipendence:'+'\n', "blue")]
        if len(errors)==0:
            log.append(('CPI holds'+'\n', "green"))
        else:
            missing_indipendence = []
            ltsi_error = [("CLOSURE UNDER CPI CANNOT BE PERFORMED!"+'\n', "red")]
            print_error = False
            for edge1, edge2, rev, edge in errors:
                if rev == edge:
                    print_error = True
                    ltsi_error.append(("- The relation ", "black"))
                    ltsi_error.append((EdgeToString(edge1)+" ι "+EdgeToString(edge2), "green"))
                    ltsi_error.append((" would imply ", "black"))
                    ltsi_error.append((EdgeToString(rev)+" ι "+EdgeToString(edge), "red"))
                    ltsi_error.append((", but this is ", "black"))
                    ltsi_error.append(("not possible", "red"))
                    ltsi_error.append((" since independence is irreflexive"+'\n', "black"))
                else:
                    missing_indipendence.append(("- ", "black")) 
                    missing_indipendence.append((EdgeToString(edge1)+' ι '+EdgeToString(edge2), "green"))
                    missing_indipendence.append((' but not ', "black"))
                    missing_indipendence.append((EdgeToString(rev)+" ι "+EdgeToString(edge)+'\n', "red"))
            
            log.extend(ltsi_error if print_error else missing_indipendence)
        log.append(('\n', "black"))
        return log