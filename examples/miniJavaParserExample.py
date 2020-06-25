# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse
"""

import re
import sys
import argparse

from mitos.core    import Parser, PrettyPrinter, Lexer
from mitos.writers import LexerWriter, ParserWriter


if __name__ == '__main__':
    # Generates the ebnf results
    testFileName = 'grammars/miniJava.ebnf'

    try:
      with open(testFileName, 'r') as testFile:
          testFileData = testFile.readlines()
    except FileNotFoundError:
      print('Error: test file {} does not exist'.format(testFileName))
      sys.exit()

    lexer = Lexer()
    lexems = lexer.lex(testFileData)

    verbose = True
    parser = Parser(verbose)
    grammar = parser.parse(lexems)

    writer = LexerWriter("results/miniJava/MiniJavaLexer.py")
    writer.visit(grammar)
    writer.write(writer.lexemList)

    writerParser = ParserWriter(writer.lexemList,"results/miniJava/MiniJavaParser.py")
    writerParser.visit(grammar)

    pp = PrettyPrinter("results/miniJava/mini_java_grammar_pp.ebnf")
    pp.visit(grammar)
