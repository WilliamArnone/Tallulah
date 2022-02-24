import copy
from distutils.log import error
from Graph import EdgeToString, Graph, ReverseEdge

class CIRE:

    name = "CIRE - Coinitial Independence Respects Event"

    def Check(graph:Graph):
        """Check property and return true if holds"""
        errors = []

        events = copy.deepcopy(graph.events)

        while len(events)>1:
            event1 = events.pop()
            for event2 in events:

                temp = []
                ci = False

                for edge1 in event1:
                    for edge2 in event2:
                        are_coinitial = list(edge1)[0] == list(edge2)[0]
                        are_indipendent = graph.AreIndependent(edge1, edge2)

                        ci = ci or (are_coinitial and are_indipendent)

                        if are_coinitial and not are_indipendent:
                            temp.append((edge1, edge2))

                if ci: errors.extend(temp)

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
        log.append(('['+EdgeToString(edge1)+"] ci ["+EdgeToString(edge2)+']', "green"))
        log.append((' but not', "black"))
        log.append((EdgeToString(edge1)+" ι "+EdgeToString(edge2), "red"))
        return log