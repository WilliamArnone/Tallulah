from Graph import EdgeToString, Graph, ReverseEdge

class RPI:

    name = "RPI - Reversing Preserves Independence"

    def Check(graph:Graph):
        """Check property and return true if holds"""
        errors = []
        non_applyable_errors = []

        for edge1, edge2 in graph.independence:
            #this is needed only to show non applyable errors at the top
            if ReverseEdge(edge1) == edge2:
                errors.append((edge1, edge2, True))
                errors.append((edge1, edge2, False))
                continue

            if not graph.AreIndependent(ReverseEdge(edge1), edge2):
                errors.append((edge1, edge2, True))
            if not graph.AreIndependent(edge1, ReverseEdge(edge2)):
                errors.append((edge1, edge2, False))

        non_applyable_errors.extend(errors)
        return non_applyable_errors
    
    def Apply(graph: Graph, error):
        """Remove errors from the graph"""
        edge1, edge2, first_reverse = error
        if first_reverse:
            graph.AddIndependence(ReverseEdge(edge1), edge2)
        else:
            graph.AddIndependence(ReverseEdge(edge2), edge1)

    def IsApplyable(error):
        """Return True if the error can be fixed"""
        edge1, edge2, first_reverse = error
        return ReverseEdge(edge1) != edge2

    def GetLog(error):
        """Return the error in a (text, color) list"""
        log = []
        edge1, edge2, first_reverse = error
        if first_reverse:
            normal, reverse = edge2, ReverseEdge(edge1)
        else:
            normal, reverse = edge1, ReverseEdge(edge2)

        if normal != reverse:
            log.append((EdgeToString(edge1)+" ι "+EdgeToString(edge2), "green"))
            log.append(("but not", "black"))
            log.append((EdgeToString(normal)+" ι "+EdgeToString(reverse), "red"))
        else:
            log.append((EdgeToString(edge1)+" ι "+EdgeToString(edge2), "green"))
            log.append(("but this would imply", "black"))
            log.append((EdgeToString(normal)+" ι "+EdgeToString(reverse), "red"))
            log.append(("but this is", "black"))
            log.append(("not possible", "red"))
            log.append(("since independence is irreflexive", "black"))

        return log
