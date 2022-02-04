from Graph import EdgeToString, Graph

#t: P-α->Q and u: P-β->R and t ι u  =>  exist u': Q-β->S and t': R-α->S
class SP:
    def Check(graph:Graph):
        """Check SP property and return true if holds"""
        errors = set()

        #start is the P of our definition
        for start in graph.nodes:
            edges = graph.GetEdgesFrom(start, all = False)

            #edge1 is the t of our definition
            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1

                #edge2 is the u of our definition
                for edge2 in edges:
                    (start2, label2, end2, is_forward2) = edge2
                    if graph.AreIndipendent(edge1, edge2):
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

                            found = found or firstExist or secondExist
                            if firstExist and secondExist:
                                #SP is valid, no need to search further
                                temp = []
                                break
                            elif secondExist and not firstExist:
                                #if SP doesn't hold, it's because u' is missing
                                temp.append(first)
                            elif firstExist and not secondExist:
                                #if SP doesn't hold, it's because t' is missing
                                temp.append(second)

                        if not found:
                            #there is no possible candidate for S
                            errors.add((edge1, edge2, (end1, label2, None, is_forward2)))
                            #errors.add((edge1, edge2, (end2, label1, None, is_forward1)))
                        else:
                            #store as error the previous found edges
                            for error in temp:
                                errors.add((edge1, edge2, error))

                            
        return errors
    
    def Apply(graph: Graph, errors):
        """Remove SP errors from the graph"""
        for ind1, ind2, error in errors:
            start, label, end, forward = error
            if(end != None): graph.AddEdge(error)

    def ToString(errors):
        """Returns the SP errors in a string"""
        string ='SP - Square Property:'+'\n'
        if len(errors)==0:
            string += 'SP holds'+'\n'
        else:
            for ind1, ind2, error in errors:
                start, label, end, is_forward = error
                if end == None:
                    string += '- ' + EdgeToString(ind1)+" ι "+EdgeToString(ind2)+" but they don't have any valid t' or u'"+'\n'
                    #log = log + "- "+start+" should have a "+"forward" if is_forward else "backward" +" transiction labbeled "+label+" to a state"+'\n'
                else:
                    string += '- ' + EdgeToString(ind1)+" ι "+EdgeToString(ind2)+ ' but they don\'t have a common end, could be added '+EdgeToString(error)+'\n'
        string+='\n'
        return string