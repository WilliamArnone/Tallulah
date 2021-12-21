class Graph:
    #to save memory, edges are saved in the format (start, label, end)
    #functions return edges in the format (start, label, end, is_forward) 
    
    
    def __init__(self):
        self.edges = {}
        self.events = []
        self.nodes = set()
        self.indipendence = set()
        self.startNode = 'start'
        self.nodes.add(self.startNode)

    def AddNode(self, *nodes):
        for node in nodes: self.nodes.add(node)

    def AddEdge(self, edge):
        lst = list(edge)
        start = lst[0] 
        label = lst[1]
        end = lst[2]
        is_forward = len(lst)==3 or lst[3]
        self.AddNode(start, end)
        if is_forward:
            if not (start, end) in self.edges: 
                self.edges[(start, end)] = []
            if not label in self.edges[(start, end)]:
                self.edges[(start, end)].append(label)
        else:
            if not (end, start) in self.edges: 
                self.edges[(end, start)] = []
            if not label in self.edges[(end, start)]:
                self.edges[(end, start)].append(label)

    def RemoveEdge(self, edge):
        lst = list(edge)
        start = lst[0] 
        label = lst[1]
        end = lst[2]
        is_forward = len(lst)==3 or lst[3]
        if is_forward:
            if (start, end) in self.edges:
                self.edges[(start, end)].remove(label)
        else:
            if (end, start) in self.edges:
                self.edges[(end, start)].remove(label)

    def GetEdgesFrom(self, node, all=True, only_forward=True):
        edges = []
        for end in self.nodes:
            if (node, end) in self.edges:
                forward = self.edges[(node, end)]
                for label in forward:
                    if all or only_forward: edges.append((node, label, end, True))
            if (end, node) in self.edges:
                backward = self.edges[(end, node)]
                for label in backward:
                    if all or not only_forward: edges.append((node, label, end, False))

        return edges

    def GetEdgesBetween(self, start, end, all=True, only_forward=True):
        edges = []
        if all or only_forward:
            labels = self.edges[(start,end)] if (start, end) in self.edges else []
            for label in labels: edges.append((start, label, end, True))
        if all or not only_forward:
            labels = self.edges[(end,start)] if (end, start) in self.edges else []
            for label in labels: edges.append((start, label, end, False))

        return edges
    
    def EdgeExists(self, edge):
        start, label, end, forward = edge
        if not forward: start, end = end, start
        return label in self.edges[(start, end)] if (start, end) in self.edges else False

    def GetAdj(self, node):
        nodes = []
        for end in self.nodes:
            if (node, end) in self.edges and self.edges[(node, end)]:
                nodes.append(end)

        return nodes

    def AddIndipendence(self, edge1, edge2):
        if not (edge2, edge1) in self.indipendence:
            self.indipendence.add((edge1, edge2))

    def AreIndipendent(self, edge1, edge2):
        for i in self.indipendence:
            if i == (edge1, edge2) or i == (edge2, edge1):
                return True
        return False

    def Reverse(self, edge):
        start, label, end, is_forward = edge
        return (end, label, start, not is_forward)

    def InitEvents(self):
        for start in self.nodes:
            edges = self.GetEdgesFrom(start)
            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1
                self.NewEvent(edge1)
                for edge2 in edges:
                    #is this necessary?
                    if edge1 == edge2: continue

                    (start2, label2, end2, is_forward2) = edge2
                    self.NewEvent(edge2)
                    
                    for end in self.nodes:
                        first = (end1, label2, end, is_forward2)
                        second = (end2, label1, end, is_forward1)

                        if self.EdgeExists(first) and self.EdgeExists(second):
                            cond = []
                            cond.append((edge1, edge2))
                            cond.append(((end1, label1, start, not is_forward1), 
                                (end1, label2, end, is_forward2)))
                            cond.append(((end2, label2, start, not is_forward2), 
                                (end2, label1, end, is_forward1)))
                            cond.append(((end, label2, end1, not is_forward2), 
                                (end, label1, end2, not is_forward1)))

                            indipendent = True
                            for condition in cond:
                                ind1, ind2 = condition
                                indipendent = indipendent and self.AreIndipendent(ind1, ind2)
                            
                            if indipendent and ((is_forward1 == is_forward2 and end1 != end2) or (is_forward1 == is_forward2 and start != end)):
                                    self.AddToEvent(edge1, second)
                                    self.AddToEvent(edge2, first)

                            else:
                                self.NewEvent(first)
                                self.NewEvent(second)

    def NewEvent(self, edge):
        for event in self.events:
            if edge in event: return event
        new_event = set()
        new_event.add(edge)
        self.events.append(new_event)
        return new_event

    def AddToEvent(self, edge1, edge2):
        union = set()
        event1 = None
        event2 = None
        
        for event in self.events:
            if edge1 in event: 
                event1 = event
                union = union.union(event)
            if edge2 in event: 
                event2 = event
                union = union.union(event)

        if (event1 != None): self.events.remove(event1) 
        else: union.add(edge1)
        if (event2 != None and event2 != event1): self.events.remove(event2)
        else: union.add(edge2)
        self.events.append(union)

    def AreSameEvent(self, edge1, edge2):
        for event in self.events:
            if edge1 in event: return edge2 in event
        return False

    def GetEventClass(self, edge):
        for event in self.events:
            if edge in event: return event
        return None

    def ToString(self):
        graph = 'digraph G {\n'

        edges = ''

        for start in self.nodes:
            for end in self.nodes:
                if not (start, end) in self.edges: continue
                for label in self.edges[(start, end)]:
                    if start == self.startNode:
                        graph = graph + '\t"' + start + '" -> "' + end +'" [label="'+label+'"]\n'
                    else:
                        edges = edges + '\t"' + start + '" -> "' + end +'" [label="'+label+'"]\n'
        
        graph = graph + edges + "} \n /* \n"
        
        for (start1, label1, end1, is_forward1), (start2, label2, end2, is_forward2) in self.indipendence:
            graph = graph + '\t' + ('>' if is_forward1 else '<') + start1 + ' -' + label1 + '-> '+ end1 +' / '
            graph = graph + ('>' if is_forward2 else '<') + start2 + ' -' + label2 + '-> '+ end2 +'\n'

        graph = graph + '*/'
        return graph