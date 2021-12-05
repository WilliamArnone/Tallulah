
class Graph:
    edges = set()
    nodes = set()
    labels = set()
    indipendence = set()
    
    def AddNode(self, *nodes):
        for node in nodes: self.nodes.add(node)

    def AddEdge(self, edge):
        (start, label, end) = edge
        self.AddNode(start, end)
        self.edges.add((start, label, end, True))
        self.edges.add((end, label, start, False))

    def GetAdj(self, node):
        nodes = set()
        for label in self.labels:
            for _node in self.nodes:
                if (node, label, _node, False) in self.edges | (node, label, _node, False) in self.edges:
                    nodes.add(_node)
        return nodes

    def AddIndipendence(self, node1, node2):
        self.indipendence.add((node1, node2))

    def AreIndipendent(self, node1, node2):
        for i in self.indipendence:
            if(i == (node1, node2) | i == (node2, node1)):
                return True
        return False