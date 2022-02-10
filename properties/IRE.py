from Graph import EdgeToString, Graph

#t ∼ t' ι u => t ι u
class IRE:
    def Check(graph:Graph):
        """Check IRE property and return true if holds"""
        errors = set()
        graph.InitEvents()

        #for each indipendent relation we want to check if also the edges of the same event are indipendent
        for indipendence in graph.indipendence:
            edge1, edge2 = indipendence
            event = graph.GetEventClass(edge1)
            for edge in event:
                if not graph.AreIndipendent(edge, edge2):
                    errors.add((edge1, edge, edge2))
            #we must make 2 searches, one for edge1 and one for edge2
            event = graph.GetEventClass(edge2)
            for edge in event:
                if not graph.AreIndipendent(edge, edge1):
                    errors.add((edge2, edge, edge1))
        return errors

    def Apply(graph: Graph, errors):
        """Remove IRE errors from the graph"""
        for ev, edge1, edge2 in errors:
            graph.AddIndipendence(edge1, edge2)

    def ToString(errors):
        """Returns the IRE errors in a string"""

        log = [('IRE - Independence Respects Events:'+'\n', "blue")]
        if len(errors)==0:
            log.append(('IRE holds'+'\n', "green"))
        else:
            for ind, edge1, edge2 in errors:
                log.append(("- ", "black"))
                log.append((EdgeToString(edge1)+" ~ "+EdgeToString(ind)+" ι "+EdgeToString(edge2), "green"))
                log.append((" but not ", "black"))
                log.append((EdgeToString(edge1)+' ι '+EdgeToString(edge2)+'\n', "red"))
        
        log.append(('\n', "black"))
        return log