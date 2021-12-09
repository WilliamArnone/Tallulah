# Generated from DOT.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DOTParser import DOTParser
else:
    from DOTParser import DOTParser

# This class defines a complete listener for a parse tree produced by DOTParser.
class DOTListener(ParseTreeListener):

    # Enter a parse tree produced by DOTParser#graph.
    def enterGraph(self, ctx:DOTParser.GraphContext):
        pass

    # Exit a parse tree produced by DOTParser#graph.
    def exitGraph(self, ctx:DOTParser.GraphContext):
        pass


    # Enter a parse tree produced by DOTParser#stmt_list.
    def enterStmt_list(self, ctx:DOTParser.Stmt_listContext):
        pass

    # Exit a parse tree produced by DOTParser#stmt_list.
    def exitStmt_list(self, ctx:DOTParser.Stmt_listContext):
        pass


    # Enter a parse tree produced by DOTParser#indipendence_list.
    def enterIndipendence_list(self, ctx:DOTParser.Indipendence_listContext):
        pass

    # Exit a parse tree produced by DOTParser#indipendence_list.
    def exitIndipendence_list(self, ctx:DOTParser.Indipendence_listContext):
        pass


    # Enter a parse tree produced by DOTParser#stmt.
    def enterStmt(self, ctx:DOTParser.StmtContext):
        pass

    # Exit a parse tree produced by DOTParser#stmt.
    def exitStmt(self, ctx:DOTParser.StmtContext):
        pass


    # Enter a parse tree produced by DOTParser#attr_stmt.
    def enterAttr_stmt(self, ctx:DOTParser.Attr_stmtContext):
        pass

    # Exit a parse tree produced by DOTParser#attr_stmt.
    def exitAttr_stmt(self, ctx:DOTParser.Attr_stmtContext):
        pass


    # Enter a parse tree produced by DOTParser#attr_list.
    def enterAttr_list(self, ctx:DOTParser.Attr_listContext):
        pass

    # Exit a parse tree produced by DOTParser#attr_list.
    def exitAttr_list(self, ctx:DOTParser.Attr_listContext):
        pass


    # Enter a parse tree produced by DOTParser#attr_label.
    def enterAttr_label(self, ctx:DOTParser.Attr_labelContext):
        pass

    # Exit a parse tree produced by DOTParser#attr_label.
    def exitAttr_label(self, ctx:DOTParser.Attr_labelContext):
        pass


    # Enter a parse tree produced by DOTParser#a_list.
    def enterA_list(self, ctx:DOTParser.A_listContext):
        pass

    # Exit a parse tree produced by DOTParser#a_list.
    def exitA_list(self, ctx:DOTParser.A_listContext):
        pass


    # Enter a parse tree produced by DOTParser#a_label.
    def enterA_label(self, ctx:DOTParser.A_labelContext):
        pass

    # Exit a parse tree produced by DOTParser#a_label.
    def exitA_label(self, ctx:DOTParser.A_labelContext):
        pass


    # Enter a parse tree produced by DOTParser#start.
    def enterStart(self, ctx:DOTParser.StartContext):
        pass

    # Exit a parse tree produced by DOTParser#start.
    def exitStart(self, ctx:DOTParser.StartContext):
        pass


    # Enter a parse tree produced by DOTParser#start_node.
    def enterStart_node(self, ctx:DOTParser.Start_nodeContext):
        pass

    # Exit a parse tree produced by DOTParser#start_node.
    def exitStart_node(self, ctx:DOTParser.Start_nodeContext):
        pass


    # Enter a parse tree produced by DOTParser#start_edge.
    def enterStart_edge(self, ctx:DOTParser.Start_edgeContext):
        pass

    # Exit a parse tree produced by DOTParser#start_edge.
    def exitStart_edge(self, ctx:DOTParser.Start_edgeContext):
        pass


    # Enter a parse tree produced by DOTParser#edge_stmt.
    def enterEdge_stmt(self, ctx:DOTParser.Edge_stmtContext):
        pass

    # Exit a parse tree produced by DOTParser#edge_stmt.
    def exitEdge_stmt(self, ctx:DOTParser.Edge_stmtContext):
        pass


    # Enter a parse tree produced by DOTParser#edgeRHS.
    def enterEdgeRHS(self, ctx:DOTParser.EdgeRHSContext):
        pass

    # Exit a parse tree produced by DOTParser#edgeRHS.
    def exitEdgeRHS(self, ctx:DOTParser.EdgeRHSContext):
        pass


    # Enter a parse tree produced by DOTParser#node_stmt.
    def enterNode_stmt(self, ctx:DOTParser.Node_stmtContext):
        pass

    # Exit a parse tree produced by DOTParser#node_stmt.
    def exitNode_stmt(self, ctx:DOTParser.Node_stmtContext):
        pass


    # Enter a parse tree produced by DOTParser#node_id.
    def enterNode_id(self, ctx:DOTParser.Node_idContext):
        pass

    # Exit a parse tree produced by DOTParser#node_id.
    def exitNode_id(self, ctx:DOTParser.Node_idContext):
        pass


    # Enter a parse tree produced by DOTParser#port.
    def enterPort(self, ctx:DOTParser.PortContext):
        pass

    # Exit a parse tree produced by DOTParser#port.
    def exitPort(self, ctx:DOTParser.PortContext):
        pass


    # Enter a parse tree produced by DOTParser#subgraph_stmt.
    def enterSubgraph_stmt(self, ctx:DOTParser.Subgraph_stmtContext):
        pass

    # Exit a parse tree produced by DOTParser#subgraph_stmt.
    def exitSubgraph_stmt(self, ctx:DOTParser.Subgraph_stmtContext):
        pass


    # Enter a parse tree produced by DOTParser#assignment.
    def enterAssignment(self, ctx:DOTParser.AssignmentContext):
        pass

    # Exit a parse tree produced by DOTParser#assignment.
    def exitAssignment(self, ctx:DOTParser.AssignmentContext):
        pass


    # Enter a parse tree produced by DOTParser#indipendence.
    def enterIndipendence(self, ctx:DOTParser.IndipendenceContext):
        pass

    # Exit a parse tree produced by DOTParser#indipendence.
    def exitIndipendence(self, ctx:DOTParser.IndipendenceContext):
        pass


    # Enter a parse tree produced by DOTParser#indipendence_edge.
    def enterIndipendence_edge(self, ctx:DOTParser.Indipendence_edgeContext):
        pass

    # Exit a parse tree produced by DOTParser#indipendence_edge.
    def exitIndipendence_edge(self, ctx:DOTParser.Indipendence_edgeContext):
        pass


    # Enter a parse tree produced by DOTParser#identifier.
    def enterIdentifier(self, ctx:DOTParser.IdentifierContext):
        pass

    # Exit a parse tree produced by DOTParser#identifier.
    def exitIdentifier(self, ctx:DOTParser.IdentifierContext):
        pass



del DOTParser