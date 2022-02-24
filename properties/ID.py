from distutils.log import error
from Graph import EdgeToString, Graph, ReverseEdge

class ID:

    name = "ID - Independence of Diamonds"

    def Check(graph:Graph):
        """Check property and return true if holds"""
        errors = []

        for start in graph.nodes:
            edges = graph.GetEdgesFrom(start)

            while len(edges)>1:
                edge1 = edges.pop()

                (start1, label1, end1, is_forward1) = edge1
                for edge2 in edges:
                    (start2, label2, end2, is_forward2) = edge2
                    
                    for end in graph.nodes:
                        first = (end1, label2, end, is_forward2)
                        second = (end2, label1, end, is_forward1)

                        # searching for diamonds
                        if graph.EdgeExists(first) and graph.EdgeExists(second) and (
                            (is_forward1 == is_forward2 and end1 != end2) or (is_forward1 != is_forward2 and start != end)
                            ) and not graph.AreIndependent(edge1, edge2):
                            errors.append((edge1, edge2))
        
        return errors
    
    def Apply(graph: Graph, error):
        """Remove errors from the graph"""
        edge1, edge2 = error
        graph.AddIndependence(edge1, edge2)

    def IsApplyable(error):
        """Return True if the error can be fixed"""
        return True

    def GetLog(error):
        """Return the error in a (text, color) list"""
        edge1, edge2 = error
        log = []

        log.append((EdgeToString(edge1)+" and "+EdgeToString(edge2) + "are part of a commuting diamond", "green"))
        log.append(("but", "black"))
        log.append(("they are not independent", "red"))

        return log