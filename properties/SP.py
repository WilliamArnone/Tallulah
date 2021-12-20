from Graph import Graph

def CheckSP(graph:Graph, errors = None):
        if errors == None: errors = set()
        for node in graph.nodes:
            #remove all=False to check also backward transitions
            edges = graph.GetEdgesFrom(node, all=False)
            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1
                for edge2 in edges:
                    (start2, label2, end2, is_forward2) = edge2
                    if graph.AreIndipendent(edge1, edge2):
                        found = False
                        firstForward = is_forward1 if (is_forward1==is_forward2) else not is_forward1
                        secondForward = is_forward2 if (is_forward1==is_forward2) else not is_forward2
                        for s in graph.nodes:
                            first_start, first_end = (end1, s) if firstForward else (s, end1)
                            second_start, second_end = (end2, s) if secondForward else (s, end2)

                            first = (first_start, label2, first_end, firstForward)
                            second = (second_start, label1, second_end, secondForward)

                            firstExist = graph.EdgeExists(first) 
                            secondExist = graph.EdgeExists(second)

                            if firstExist or secondExist:
                                found = True
                                if not firstExist:
                                    errors.add((end1, label2, s, firstForward))
                                elif not secondExist:
                                    errors.add((end2, label1, s, secondForward))

                        if not found:
                            errors.add((end1, label2, None, firstForward))
                            errors.add((end2, label1, None, secondForward))

                        
        return len(errors)==0