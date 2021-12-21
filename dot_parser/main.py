from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import ParseTreeWalker
from .DOTLexer import DOTLexer
from .DOTParser import DOTParser
from .MyErrorListener import MyErrorListener
from antlr4.FileStream import FileStream
from antlr4.CommonTokenStream import CommonTokenStream

from .GraphBuilder import GraphBuilder


def main(path_file):
    input_stream = FileStream(path_file)
    
    lexer = DOTLexer(input_stream)
    stream = CommonTokenStream(lexer)

    parser = DOTParser(stream)
    
    parser.removeErrorListeners()
    lexer.removeErrorListeners()

    errorListener = MyErrorListener()
    
    parser.addErrorListener(errorListener)
    lexer.addErrorListener(errorListener)
    
    try:
        tree = parser.graph()
        
        builder = GraphBuilder()
        walker = ParseTreeWalker()
        walker.walk(builder, tree)
    except:
        return (None, errorListener.errors)

    builder.graph.InitEvents()
    return (builder.graph, [])
