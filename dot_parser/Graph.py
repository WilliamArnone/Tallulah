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
            if not (start, end) in self.edges.keys(): 
                self.edges[(start, end)] = []
            if not label in self.edges[(start, end)]:
                self.edges[(start, end)].append(label)
        else:
            if not (end, start) in self.edges.keys(): 
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
            if (start, end) in self.edges.keys():
                self.edges[(start, end)].remove(label)
        else:
            if (end, start) in self.edges.keys():
                self.edges[(end, start)].remove(label)

    def GetEdgesFrom(self, node, all=True, is_forward=True):
        edges = []
        for end in self.nodes:
            if (node, end) in self.edges.keys():
                forward = self.edges[(node, end)]
                for label in forward:
                    if all or is_forward: edges.append((node, label, end, True))
            if (end, node) in self.edges.keys():
                backward = self.edges[(end, node)]
                for label in backward:
                    if all or not is_forward: edges.append((node, label, end, False))

        return edges

    def GetAdj(self, node):
        nodes = []
        for end in self.nodes:
            if (node, end) in self.edges.keys() and self.edges[(node, end)]:
                nodes.append(end)

        return nodes

    def AddIndipendence(self, edge1, edge2):
        self.indipendence.add((edge1, edge2))

    def AreIndipendent(self, node1, node2):
        for i in self.indipendence:
            if i == (node1, node2) or i == (node2, node1):
                return True
        return False

    def CheckWF(self, errors = None, node = None, visited=None):

        if errors == None: errors = []
        if visited == None: visited = []
        if node == None: node = self.startNode

        if node in visited: return False

        visited.append(node)
        for adj_node in self.GetAdj(node):
            if not self.CheckWF(errors, adj_node, visited): 
                for label in self.edges[(node, adj_node)]:
                    errors.append((node, label, adj_node, True))

        visited.remove(node)

        return len(errors)==0 if len(visited)==0 else True


    def CheckSP(self, errors = None):
        if errors == None: errors = []
        for node in self.nodes:
            edges = self.GetEdgesFrom(node, all=False)
            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1
                for edge2 in edges:
                    (start2, label2, end2, is_forward2) = edge2
                    if self.AreIndipendent(edge1, edge2):
                        for s in self.nodes:
                            firstExist = (end1, s) in self.edges.keys() and label2 in self.edges[(end1, s)] 
                            secondExist = (end2, s) in self.edges.keys() and label1 in self.edges[(end2, s)]

                            if firstExist or secondExist:
                                if not firstExist:
                                    errors.append((end1, label2, s, True))
                                elif not secondExist:
                                    errors.append((end2, label1, s, True))
                        
        return len(errors)==0

    def CheckBTI(self, errors = None):
        if errors == None: errors = []
        for node in self.nodes:
            edges = self.GetEdgesFrom(node, all=False, is_forward=False)
            for edge1 in edges:
                for edge2 in edges:
                    if edge1 != edge2 and not self.AreIndipendent(edge1, edge2):
                        errors.append((edge1, edge2))
        return len(errors)==0

    def ToString(self):
        graph = 'digraph G {\n'

        edges = ''

        for start in self.nodes:
            for end in self.nodes:
                if not (start, end) in self.edges.keys(): continue
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