import re
import sys
import argparse
from lexer import Lexer
from parser import Parser
#from visitor import Visitor
from lexerWriterV2 import LexerWriter
from parserWriter import ParserWriter
from prettyprinter import PrettyPrinter

if __name__ == '__main__':
    # Generates the Pascal results
    testFileName = 'grammars/pascal_grammar.ebnf'

    try:
      with open(testFileName, 'r') as testFile:
          testFileData = testFile.readlines()
    except FileNotFoundError:
      print('Error: test file {} does not exist'.format(testFileName))
      sys.exit()

    lexer = Lexer()
    lexems = lexer.lex(testFileData)

    verbose = False
    parser = Parser(verbose)
    grammar = parser.parse(lexems)

    writer = LexerWriter("results/Pascal/PascalLexer_fromJinja.py")
    writer.visit(grammar)
    writer.write(writer.lexemList)

    writerParser = ParserWriter(writer.lexemList,"results/Pascal/PascalParser_fromJinja.py")
    writerParser.visit(grammar)

    pp = PrettyPrinter("results/Pascal/pascal_grammar_pp.ebnf")
    pp.visit(grammar)
