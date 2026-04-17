import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from generated.WhileLangLexer import WhileLangLexer
from generated.WhileLangParser import WhileLangParser
from semantic_analyzer.SemanticVisitor import SemanticVisitor

class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"Error de sintaxis en la línea {line}:{column} - {msg}")

def analyze(code):
    try:
        input_stream = InputStream(code)
        lexer = WhileLangLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyErrorListener())
        stream = CommonTokenStream(lexer)
        parser = WhileLangParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyErrorListener())
        tree = parser.program()
        visitor = SemanticVisitor()
        visitor.errors = 0
        visitor.visit(tree)
        if visitor.errors == 0:
            print("Análisis completado sin errores semánticos.")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            analyze(f.read())
    else:
        print("Uso: python main.py <archivo>")
