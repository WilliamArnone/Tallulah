from Graph import Graph

def CheckSP(graph:Graph, errors:set = None):
    if errors == None: errors = set()
    for start in graph.nodes:
        #remove all=False to check also backward transitions
        #only forward transictions?
        edges = graph.GetEdgesFrom(start, all = False)
        for edge1 in edges:
            (start1, label1, end1, is_forward1) = edge1
            for edge2 in edges:
                (start2, label2, end2, is_forward2) = edge2
                if graph.AreIndipendent(edge1, edge2):
                    found = False
                    temp = []
                    for end in graph.nodes:
                        first = (end1, label2, end, is_forward2)
                        second = (end2, label1, end, is_forward1)

                        firstExist = graph.EdgeExists(first) 
                        secondExist = graph.EdgeExists(second)

                        found = found or firstExist or secondExist
                        if firstExist and secondExist:
                            temp = []
                            break
                        elif not firstExist:
                            temp.append(first)
                        elif not secondExist:
                            temp.append(second)

                    if not found:
                        errors.add((end1, label2, None, is_forward2))
                        errors.add((end2, label1, None, is_forward1))
                    else:
                        for error in temp:
                            errors.add(error)

                        
    return len(errors)==0