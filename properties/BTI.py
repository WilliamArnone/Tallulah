from Graph import EdgeToString, Graph

#t: P~α~>Q and t': P~β~>Q' and t=/=t'  =>  t ι t'
class BTI:
    
    name = "BTI - Backward Transitions are Independent"

    def Check(graph:Graph):
        """Check BTI property and return true if holds"""
        errors = set()

        #node is the P of the definition
        for node in graph.nodes:
            edges = graph.GetEdgesFrom(node, all=False, only_forward=False)

            #edge1 is the t of the definition
            while len(edges)>0:
                edge1 = edges.pop()
                #edge2 is the u of the definition
                for edge2 in edges:
                    #t and u are coinitial, so if they are not the same edge they must be independent
                    if edge1 != edge2 and not graph.AreIndependent(edge1, edge2):
                        errors.add((edge1, edge2))
        return list(errors)

    def Apply(graph: Graph, error):
        """Remove BTI errors from the graph"""
        edge1, edge2 = error
        graph.AddIndependence(edge1, edge2)

    def IsApplyable(error):
        """Returns True if the error can be fixed"""
        return True

    def GetLog(error):
        """Returns the BTI errors in a (text, color) list"""
        log = []
        edge1, edge2 = error
        log.append((EdgeToString(edge1), "red"))
        log.append((' and ', "black"))
        log.append((EdgeToString(edge2), "red"))
        log.append((' are ', "black"))
        log.append(('not independent', "red"))
        return log