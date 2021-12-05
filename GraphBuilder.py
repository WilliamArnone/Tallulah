from DOTParser import DOTParser
from DOTListener import DOTListener



class GraphBuilder(DOTListener):
    def enterEdge_stmt(self, ctx:DOTParser.Edge_stmtContext):
        print("Edge encountered")

    def enterA_label(self, ctx:DOTParser.A_labelContext):
        print("Label")

    def enterIndipendence_comment(self, ctx:DOTParser.Indipendence_commentContext):
        print(ctx.getText())
