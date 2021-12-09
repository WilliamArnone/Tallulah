from DOTParser import DOTParser
from DOTListener import DOTListener
from Graph import Graph


class GraphBuilder(DOTListener):

    graph = Graph()
    nodes_order = []
    nodes_depth = []
    edges = []
    labels = []

    def enterEdge(self):        
        self.nodes_order.append(set())
        self.nodes_depth.append(set())
        self.edges.append(set())

    def exitEdge(self):
        label = self.labels.pop()
        self.nodes_order.pop()
        nodes = self.nodes_depth.pop()
        if self.nodes_depth:
            for node in nodes: self.nodes_depth[-1].add(node)
            
        for edge in self.edges.pop():
            lst = list(edge)
            self.graph.AddEdge((lst[0], label, lst[1]))

    def enterStart_edge(self, ctx:DOTParser.Start_edgeContext):
        self.enterEdge()

    def exitStart_edge(self, ctx:DOTParser.Start_edgeContext):
        self.exitEdge()


    def enterEdge_stmt(self, ctx:DOTParser.Edge_stmtContext):
        self.enterEdge()


    def exitEdge_stmt(self, ctx:DOTParser.Edge_stmtContext):
        self.exitEdge()
        
    def enterSubgraph_stmt(self, ctx:DOTParser.Subgraph_stmtContext):
        self.nodes_depth.append(set())
        self.nodes_order.append(set())
        self.edges.append(set())

    def exitSubgraph_stmt(self, ctx:DOTParser.Subgraph_stmtContext):
        nodes = self.nodes_depth.pop()
        self.nodes_order.pop()
        if self.nodes_order and self.nodes_depth:
            for node in nodes: 
                self.nodes_depth[-1].add(node)
                self.nodes_order[-1].add(node)
        self.edges.pop()

    def enterNode_id(self, ctx:DOTParser.Node_idContext):
        if(self.nodes_depth and self.nodes_order):
            node = ctx.getText().replace('"',"")
            self.nodes_order[-1].add(node)
            self.nodes_depth[-1].add(node)

    def enterEdgeRHS(self, ctx:DOTParser.EdgeRHSContext):
        self.nodes_order.append(set())

    # Exit a parse tree produced by DOTParser#edgeRHS.
    def exitEdgeRHS(self, ctx:DOTParser.EdgeRHSContext):
        end_nodes = self.nodes_order.pop()
        start_nodes = self.nodes_order[-1]
        for start in start_nodes:
            for end in end_nodes:
                self.edges[-1].add((start, end))

    def enterA_label(self, ctx:DOTParser.A_labelContext):
        self.labels.append(ctx.children[2].getText())


    def enterIndipendence(self, ctx:DOTParser.IndipendenceContext):
        self.indipendence = []


    def exitIndipendence(self, ctx:DOTParser.IndipendenceContext):
        self.graph.AddIndipendence(self.indipendence[0],self.indipendence[1])


    def enterIndipendence_edge(self, ctx:DOTParser.Indipendence_edgeContext):
        start = ctx.children[1].getText().replace('"', "")
        label = ctx.children[3].getText().replace('"', "")
        end = ctx.children[5].getText().replace('"', "")
        is_forward = ctx.children[0].getText()=='>'
        self.indipendence.append((start, label, end, is_forward))
