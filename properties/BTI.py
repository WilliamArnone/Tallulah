from Graph import EdgeToString, Graph

#t: P~α~>Q and t': P~β~>Q' and t=/=t'  =>  t ι t'
class BTI:
    def Check(graph:Graph):
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

    def Apply(graph: Graph, errors):
        """Remove BTI errors from the graph"""
        for error in errors:
            edge1, edge2 = error
            graph.AddIndipendence(edge1, edge2)

    def ToString(errors):
        """Returns the BTI errors in a string"""

        log = [('BTI - Backward Transitions are Indipendent:'+'\n', "blue")]
        if len(errors)==0:
            log.append(('BTI holds'+'\n', "green"))
        else:
            for edge1, edge2 in errors:
                log.append(("- ", "black"))
                log.append((EdgeToString(edge1), "red"))
                log.append((' and ', "black"))
                log.append((EdgeToString(edge2), "red"))
                log.append((' are ', "black"))
                log.append(('not indipendent'+'\n', "red"))
        log.append(('\n', "black"))
        return log