# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


import re
import sys

class LexemDictionary(object):
    '''
    A basic lexem dictionary that will be fed to the lexer writer and
    used as a basis to find already known lexems.
    '''

    regexExpressions = [
        # White space
        # (r'[\t]+', None),
        # (r'[ ]+', None),
        (r'[\n]+',   None),
        # Punctuation
        (r'\:\=',   ':='),
        (r'\&\&',   '&&'),
        (r'\<\=',   '<='),
        (r'\>\=',   '>='),
        (r'\!\=',   '!='),
        (r'\|\|',   '||'),
        (r'\-\-',   '--'),
        (r'\-\=',   '-='),
        (r'\+\+',   '++'),
        (r'\+\=',   '+='),
        (r'\=\=',   '=='),
        (r'\(',   '('),
        (r'\)',   ')'),
        (r'\{',   '{'),
        (r'\}',   '}'),
        (r'\[', '['),
        (r'\]',   ']'),
        (r'\;' ,  ';'),
        (r'\:',   ':'),
        (r'\,',   ','),
        (r'\.',   '.'),
        (r'\=',   '='),
        (r'\+',   '+'),
        (r'\-',   '-'),
        (r'\!',   '!'),
        (r'\?',   '?'),
        (r'\*',   '*'),
        (r'\/',   '/'),
        (r'\<<',   '<<'),
        (r'\>\>',   '>>'),
        (r'\<',   '<'),
        (r'\>',   '>'),
        (r'\&',   '&'),
        (r'\|',    '|'),
        (r'\\',   '\\'),
        (r'\/',   '/'),
        (r'\'',   "'"),
        (r'\"',   '"')
    ]

    def associateExpression(self,expression):
        match = None
        for tokenTuple in lexemDictionary:
            pattern, tag = tokenTuple
            regex = re.compile(pattern)
            match = regex.match(line, position)
            if match:
                data = match.group(0)
                if tag:
                    return tokenTuple
                break
            if not match:
                print(inputText[position])
                print("No match")
                sys.exit(1)
