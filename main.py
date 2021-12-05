from antlr4.tree.Tree import ParseTreeWalker
from DOTLexer import DOTLexer
from DOTParser import DOTParser
from antlr4.FileStream import FileStream
from antlr4.CommonTokenStream import CommonTokenStream

from GraphBuilder import GraphBuilder


def main():
    input_stream = FileStream("./Tesi/file.gv")
    
    lexer = DOTLexer(input_stream)
    stream = CommonTokenStream(lexer)
    
    parser = DOTParser(stream)
    
    tree = parser.graph()
    
    builder = GraphBuilder()
    walker = ParseTreeWalker()
    walker.walk(builder, tree)

if __name__ == main():
    main()