from Graph import Graph

def CheckCPI(graph:Graph, errors):
        if errors == None: errors = set()
        for node in graph.nodes:
            edges = graph.GetEdgesFrom(node, all=False)
            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1
                for edge2 in edges:
                    #is this necessary?
                    if edge1 == edge2: continue

                    (start2, label2, end2, is_forward2) = edge2
                    for s in graph.nodes:
                        firstExist = graph.EdgeExists((end1, label2, s, True))
                        secondExist = graph.EdgeExists((end2, label1, s, True))

                        if firstExist and secondExist:
                            cond = []
                            temp = []
                            cond.append((edge1, edge2))
                            cond.append(((end1, label1, start1, False), 
                                (end1, label2, s, True)))
                            cond.append(((end2, label2, start2, False), 
                                (end2, label1, s, True)))
                            cond.append(((s, label2, end1, False), 
                                (s, label1, end2, False)))

                            for condition in cond:
                                first, second = condition
                                if not graph.AreIndipendent(first, second): temp.append(condition)

                            if len(temp) > 0 and len(temp) < 4:
                                for condition in temp:
                                    errors.add(condition)
                        
        return len(errors)==0