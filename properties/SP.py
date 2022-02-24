from Graph import EdgeToString, Graph

#t: P-α->Q and u: P-β->R and t ι u  =>  exist u': Q-β->S and t': R-α->S
class SP:
    
    name = "SP - Square Property"
    
    def Check(graph:Graph):
        """Check SP property and return true if holds"""
        errors = []

        #used to avoid duplicate new nodes
        new_nodes = []

        #start is the P of our definition
        for start in graph.nodes:
            edges = graph.GetEdgesFrom(start)

            #edge1 is the t of our definition
            while len(edges)>0:
                edge1 = edges.pop()
                (start1, label1, end1, is_forward1) = edge1

                #edge2 is the u of our definition
                for edge2 in edges:
                    (start2, label2, end2, is_forward2) = edge2
                    if graph.AreIndependent(edge1, edge2):
                        #we need found to check if there is any node S that follows the axiom
                        found = False
                        #temp contains the possible edges to add if SP doesn't hold
                        temp = []

                        #end is the S of our definition
                        for end in graph.nodes:
                            #first is the u' of the definition
                            first = (end1, label2, end, is_forward2)
                            #second is the t' of the definition
                            second = (end2, label1, end, is_forward1)

                            firstExist = graph.EdgeExists(first) 
                            secondExist = graph.EdgeExists(second)

                            if firstExist and secondExist:
                                #SP is valid, no need to search further
                                found = True
                                break
                            elif secondExist and not firstExist:
                                #if SP doesn't hold, it's because u' is missing
                                temp.append(first)
                            elif firstExist:
                                #if SP doesn't hold, it's because t' is missing
                                temp.append(second)

                        if not found:
                            counter = 0
                            while str(counter) in graph.nodes or counter in new_nodes: counter+=1
                            new_nodes.append(counter)

                            errors.append((edge1, edge2, (end1, label2, str(counter), is_forward2), True))
                            errors.append((edge1, edge2, (end2, label1, str(counter), is_forward1), True))

                            #store as error the previous found edges
                            for error in temp:
                                errors.append((edge1, edge2, error, False))
            
        return errors
    
    def Apply(graph: Graph, error):
        """Remove SP error from the graph"""
        ind1, ind2, edge, is_new_end = error
        graph.AddEdge(edge)

    def IsApplyable(error):
        """Return True if the error can be fixed"""
        return True

    def GetLog(error):
        """Return the BTI error in a (text, color) list"""
        ind1, ind2, edge, is_new_end = error
        log = []
        start, label, end, is_forward = edge
        if is_new_end:
            log.append((EdgeToString(ind1)+" ι "+EdgeToString(ind2), "green"))
            log.append(("but they", "black"))
            log.append(("don't have any valid t' or u'", "red"))
            log.append(("could be created", "black"))
            log.append((EdgeToString(edge), "blue"))
            log.append(("with the new node \""+end+"\"", "black"))
        else:
            log.append((EdgeToString(ind1)+" ι "+EdgeToString(ind2), "green"))
            log.append(('but they don\'t have a common end, could be added', "black"))
            log.append((EdgeToString(edge), "blue"))
        return log