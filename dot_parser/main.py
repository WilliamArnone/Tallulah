from antlr4.tree.Tree import ParseTreeWalker
from DOTLexer import DOTLexer
from DOTParser import DOTParser
from antlr4.FileStream import FileStream
from antlr4.CommonTokenStream import CommonTokenStream

from GraphBuilder import GraphBuilder


def main(path_file):
    input_stream = FileStream(path_file)
    
    lexer = DOTLexer(input_stream)
    stream = CommonTokenStream(lexer)
    
    parser = DOTParser(stream)
    
    tree = parser.graph()
    
    builder = GraphBuilder()
    walker = ParseTreeWalker()
    walker.walk(builder, tree)
    return builder.graph

if __name__ == main():
    main()