
class Graph:
    #to save memory, edges are saved in the format (start, label, end)
    #functions return edges in the format (start, label, end, is_forward) 
    edges = set()
    nodes = set()
    labels = set()
    indipendence = set()
    
    def __init__(self):
        self.startNode = "start"
        self.nodes.add(self.startNode)

    def AddNode(self, *nodes):
        for node in nodes: self.nodes.add(node)

    def AddEdge(self, edge):
        (start, label, end) = edge
        self.AddNode(start, end)
        self.edges.add((start, label, end))

    def GetEdgesFrom(self, node, all=True, is_forward=True):
        edges = set()
        for edge in self.edges:
            (start, label, end) = edge
            if start == node:
                if all or is_forward: edges.add((start, label, end, True))
                if all or not is_forward: edges.add((end, label, start, False))

        return edges

    def GetAdj(self, node):
        nodes = set()
        for edge in self.edges:
            (start, label, end) = edge
            if node == start: nodes.add(end)

        return nodes

    def AddIndipendence(self, node1, node2):
        self.indipendence.add((node1, node2))

    def AreIndipendent(self, node1, node2):
        for i in self.indipendence:
            if i == (node1, node2) or i == (node2, node1):
                return True
        return False

    def CheckWF(self, node = None, visited=None):

        if visited == None: visited = []
        if node == None: node = 'A'#self.startNode
        if node in visited: return False

        visited.append(node)
        for adj_nodes in self.GetAdj(node):
            if not self.CheckWF(adj_nodes, visited): 
                return False
        visited.remove(node)
        return True


    def CheckSP(self):
        SP = True
        for node in self.nodes:
            edges = self.GetEdgesFrom(node, all=False)
            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1
                for edge2 in edges:
                    (start2, label2, end2, is_forward2) = edge2
                    if self.AreIndipendent(edge1, edge2):
                        SP = False
                        for s in self.nodes:
                            if (end1, label2, s, False) in self.edges and (end2, label1, s, False) in self.edges:
                                SP = True
                        if not SP: return False
        return SP

    def CheckBTI(self):
        BTI = True
        for node in self.nodes:
            edges = self.GetEdgesFrom(node, all=False, is_forward=False)
            for edge1 in edges:
                for edge2 in edges:
                    if edge1 == edge2: continue
                    BTI = BTI and self.AreIndipendent(edge1, edge2)
        return BTI