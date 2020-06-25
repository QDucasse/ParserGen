# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


import re
from jinja2 import Environment, FileSystemLoader

from parserGenerator.core    import Visitor
from parserGenerator.writers import LexemDictionary

class LexerWriter(Visitor):
    '''
    Lexer writer creating a lexer from a program ast
    --> inherits from Visitor
    The only two important classes that are visited are :
    - Terminal string with single quotes
    - Terminal string with double quotes
    as they are the lexems of the parsed grammar
    '''
    TEMPLATES_FOLDER="parserGenerator/templates"

    def __init__(self,name="results/lexerWriter/lexerWriter_output.py"):
        self.lexemDictionary = LexemDictionary()
        self.lexemList = [(r'[\n]+', "None")]
        self.name=name

    def write(self,lexemList):
        '''
        Writing lexems inside of the Jinja template
        '''
        file_loader = FileSystemLoader(self.TEMPLATES_FOLDER) # Getting into the correct
        env = Environment(loader=file_loader)
        template = env.get_template('lexerTemplate.j2') # Opening the template
        lex=""
        for lexem in self.lexemList[0:-1]:
            lex+='(r\''+lexem[0]+'\','+lexem[1]+'),\n\t\t'
        lex+='(r\''+lexemList[-1][0]+'\','+lexemList[-1][1]+')'
        output = template.render(lexer=lex)#On remplace les champs du template
        f=open(self.name,'w')#On écrit le résultat
        f.write(output)
        f.close()

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        '''
        Visits the terminal string and tries matching it in the lexem dictionary
        if match:
            add the already known lexem to the lexem list
        if not:
            add the new lexem to the lexem list
        '''
        lexemToTest = terminalStringSQuote.value[1:-1] # to remove quotes
        regexExpressions = self.lexemDictionary.regexExpressions
        match = None
        end = False
        for tokenRegex in regexExpressions:
            pattern, tag = tokenRegex
            regex = re.compile(pattern)
            match = regex.match(lexemToTest)
            if match:
                if (tokenRegex[0],"'"+tokenRegex[1]+"'") in self.lexemList:
                    end = True
                    break
                data = match.group(0)
                if tag:
                    self.lexemList.append((tokenRegex[0],"'"+tokenRegex[1]+"'"))
                    break
        if not(match) and not(end) and not((lexemToTest,"'"+lexemToTest+"'") in self.lexemList):
            self.lexemList.append((lexemToTest,"'" + lexemToTest + "'"))


    def visitTerminalStringDQuote(self,terminalStringDQuote):
        '''
        Same function as above as simple or double quotes do not make a difference here
        '''
        self.visitTerminalStringSQuote(terminalStringDQuote)
