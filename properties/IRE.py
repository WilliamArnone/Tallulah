from Graph import EdgeToString, Graph

#t ∼ t' ι u => t ι u
class IRE:

    name = "IRE - Independence Respects Events"

    def Check(graph:Graph):
        """Check IRE property and return true if holds"""
        errors = set()
        graph.InitEvents()

        #for each independent relation we want to check if also the edges of the same event are independent
        for independence in graph.independence:
            edge1, edge2 = independence
            event = graph.GetEventClass(edge1)
            for edge in event:
                if not graph.AreIndependent(edge, edge2):
                    errors.add((edge1, edge, edge2))
            #we must make 2 searches, one for edge1 and one for edge2
            event = graph.GetEventClass(edge2)
            for edge in event:
                if not graph.AreIndependent(edge, edge1):
                    errors.add((edge2, edge, edge1))

        #ordering errors, not fixable are on the top
        not_fixable = []
        fixable = []
        for error in errors:
            ev, edge1, edge2 = error
            if edge1==edge2: not_fixable.append(error)
            else: fixable.append(error)
        not_fixable.extend(fixable)
        
        return not_fixable

    def Apply(graph: Graph, error):
        """Remove IRE errors from the graph"""
        ev, edge1, edge2 = error
        if edge1 != edge2:
            graph.AddIndependence(edge1, edge2)

    def IsApplyable(error):
        """Return True if the error can be fixed"""
        ev, edge1, edge2 = error
        return edge1!=edge2

    def GetLog(error):
        """Return the BTI errors in a (text, color) list"""
        ind, edge1, edge2 = error
        log = []
        log.append((EdgeToString(edge1)+" ~ "+EdgeToString(ind)+" ι "+EdgeToString(edge2), "green"))
        log.append(("but not", "black"))
        log.append((EdgeToString(edge1)+' ι '+EdgeToString(edge2), "red"))
        return log