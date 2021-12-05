from DOTParser import DOTParser
from DOTListener import DOTListener
from Graph import Graph
from utils import EdgeFromCtx, IndipendenceFromCtx



class GraphBuilder(DOTListener):

    graph = Graph()
    last_edge = None

    def enterEdge_stmt(self, ctx:DOTParser.Edge_stmtContext):
        edge = EdgeFromCtx(ctx)
        self.last_edge = edge
        self.graph.AddEdge(edge)

    def exitEdge_stmt(self, ctx:DOTParser.Edge_stmtContext):
        self.last_edge = None

    def enterIndipendence_comment(self, ctx:DOTParser.Indipendence_commentContext):
        if self.last_edge == None:
            return
        (reverse, edge) = IndipendenceFromCtx(ctx)
        t = self.last_edge
        if(reverse):
            lst = list(self.last_edge)
            t = (lst[2], lst[1], lst[0])
        self.graph.AddIndipendence(t,edge)

        
