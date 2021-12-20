class Graph:
    #to save memory, edges are saved in the format (start, label, end)
    #functions return edges in the format (start, label, end, is_forward) 
    
    
    def __init__(self):
        self.edges = {}
        self.nodes = set()
        self.labels = set()
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
        self.labels.add(label)
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
        self.indipendence.add((edge1, edge2))

    def AreIndipendent(self, node1, node2):
        for i in self.indipendence:
            if i == (node1, node2) or i == (node2, node1):
                return True
        return False

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