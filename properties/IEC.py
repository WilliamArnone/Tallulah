from Graph import EdgeToString, Graph, ReverseEdge

class IEC:

    name = "IEC - Independence of Events is Coinitial"

    def Check(graph:Graph):
        """Check property and return true if holds"""
        errors = []
        non_applyable_errors = []
        already_controlled = []

        for edge1, edge2 in graph.independence:
            event1 = graph.GetEventClass(edge1)
            event2 = graph.GetEventClass(edge2)

            #check if this two events have been already controlled
            should_skip = False
            for e1, e2 in already_controlled:
                if (e1 == event1 and e2 == event2) or (e1 == event2 and e2 == event1):
                    should_skip = True
                    break
            if should_skip: continue


            temp = []
            coinitial_exists = False
            for event1edge in event1:
                for event2edge in event2:

                    are_coinitial = list(event1edge)[0]==list(event2edge)[0]
                    if graph.AreIndependent(event1edge, event2edge) and are_coinitial:
                        coinitial_exists = True
                        temp = []
                        break
                    else:
                        if event1edge!=event2edge and are_coinitial:
                            temp.append((edge1, edge2, event1edge, event2edge))

                if coinitial_exists: break
                
            already_controlled.append((event1, event2))

            if not coinitial_exists and len(temp)==0:
                non_applyable_errors.append((edge1, edge2, None, None))

            for error in temp: errors.append(error)
        
        non_applyable_errors.extend(errors)
        return non_applyable_errors
    
    def Apply(graph: Graph, error):
        """Remove errors from the graph"""
        edge1, edge2, event1edge, event2edge = error
        graph.AddIndependence(event1edge, event2edge)

    def IsApplyable(error):
        """Return True if the error can be fixed"""
        edge1, edge2, event1edge, event2edge = error
        are_coinitial = event1edge != None and event2edge != None and list(event1edge)[0]==list(event2edge)[0]
        return event1edge!=event2edge and are_coinitial

    def GetLog(error):
        """Return the error in a (text, color) list"""
        edge1, edge2, event1edge, event2edge = error

        log = []
        if event1edge==None or event2edge == None:
            log.append((EdgeToString(edge1)+" ~ "+EdgeToString(edge2)+" ι "+EdgeToString(edge2), "green"))
            log.append(("there are", "black"))
            log.append(("no coinitial independent edges", "red"))
            log.append(("and there are no coinitial edges at all", "black"))
        else:
            log.append((EdgeToString(edge1)+" ~ "+EdgeToString(edge2)+" ι "+EdgeToString(edge2), "green"))
            log.append(("there are", "black"))
            log.append(("no coinitial independent edges", "red"))
            log.append(("could be added", "black"))
            log.append((EdgeToString(event1edge)+' ι '+EdgeToString(event2edge), "red"))
        return log
