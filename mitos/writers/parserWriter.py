# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


import re

from mitos.core    import Visitor
from mitos.writers import LexemDictionary

class ParserWriter(Visitor):
    '''
    Parser writer creating a parser from a program ast
    --> inherits from Visitor
    each specific call to the visits calls the jinja rendering
    '''
    TEMPLATES_FOLDER="parserGenerator/templates"
    RESULTS_FOLDER="results/"

    def __init__(self,lexer,name="parserWriter/parserWriter_output.py"):
        self.lexer=lexer
        self.saving_file=open(name,"w")
        file_loader = FileSystemLoader(self.TEMPLATES_FOLDER) # Getting into the right directory
        self.env = Environment(loader=file_loader,extensions=['jinja2.ext.loopcontrols', 'jinja2.ext.do'])
        self.template = self.env.get_template('parser.j2') # Opening the body template
        self.output = self.template.render() # Replacing the template's fields
        self.saving_file.write(self.output)
        self.to_generate=[]
        self.first=None

    def visitGrammar(self,grammar):
        # Visits grammar
        syntax = grammar.syntax
        syntax.accept(self,syntax)
        # Template for the main parse() method
        self.template = self.env.get_template('parseMain.j2')
        self.output=self.template.render(main=self.first)
        self.saving_file.write(self.output)

    def visitSyntaxRule(self,syntaxRule):
        # Visits identifier
        id = syntaxRule.identifier
        # Visits all definitions
        defs = syntaxRule.definitions
        id.accept(self,id)
        defs.accept(self,defs)
        # Template for the different parse<element>() methods
        self.template = self.env.get_template('parseElement.j2')
        self.output=self.template.render(name=id.value.capitalize(),generator=self.to_generate[1::],n=len(self.to_generate[1::]))
        self.saving_file.write(self.output)
        #Template for testMethod()
        to_test=[] # To generate the list of char
        to_call=[] # To generate the calling of the others testMethod()
        flag=0
        flag1=True
        #if self.to_generate[1]=="opt-begin" or self.to_generate[1]=="or-begin":#While it's an optionnal seq or a OR seq we add it into the two previous list.
            #flag=1
        #print("(------------) ",id.value.capitalize())
        for i in range(len(self.to_generate)-1):
            if self.to_generate[i+1]=="opt-begin" or self.to_generate[i+1]=="or-begin":
                flag+=1
            #print(flag,self.to_generate[i+1])
            if self.to_generate[i+1][1]==1 and flag<=1 and flag1:#It's a string
                to_test.append(self.to_generate[i+1][0][1:-1])
                flag1=False
            elif self.to_generate[i+1][1]==0 and flag<=1 and flag1:#It's an identifier
                to_call.append(self.to_generate[i+1][0])
                flag1=False
            if (self.to_generate[i+1]=="or" or self.to_generate[i+1]=="opt-end") and flag==1:
                flag1=True
            if flag==0 and flag1==False:
                break
            if self.to_generate[i+1]=="opt-end" or self.to_generate[i+1]=="or-end":
                flag+=-1


        self.template = self.env.get_template('testMethod.j2')
        self.output=self.template.render(name=id.value.capitalize(),string_list=to_test,dependance_list=to_call)
        self.saving_file.write(self.output)
        self.to_generate=[]


    def visitDefinitions(self,definitions):
        # Visits all definitions
        if len(definitions.definitions)>1:
            self.to_generate.append("or-begin")
        for definition in definitions.definitions:
            definition.accept(self,definition)
            self.to_generate.append("or")
        self.to_generate=self.to_generate[0:-1]
        if len(definitions.definitions)>1:
            self.to_generate.append("or-end")

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        self.to_generate.append((terminalStringSQuote.value,1))#1=Expected , 0=For Parsing

    def visitTerminalStringDQuote(self,terminalStringDQuote):
        self.visitTerminalStringSQuote(terminalStringDQuote)

    def visitPrimary(self,primary):
        if primary.optionalSeq != None:
            self.to_generate.append("opt-begin")
            primary.optionalSeq.accept(self,primary.optionalSeq)
            self.to_generate.append("opt-end")
        elif primary.identifier != None:
            primary.identifier.accept(self,primary.identifier)
        elif primary.repeatedSeq != None:
            self.to_generate.append("rep-begin")
            primary.repeatedSeq.accept(self,primary.repeatedSeq)
            self.to_generate.append("rep-end")
        elif primary.groupedSeq != None:
            #self.to_generate.append("grp-begin")
            primary.groupedSeq.accept(self,primary.groupedSeq)
            #self.to_generate.append("grp-end")
        elif primary.specialSeq != None:
            #self.to_generate.append("spe-begin")
            primary.specialSeq.accept(self,primary.specialSeq)
            #self.to_generate.append("spe-end")
        elif primary.terminalString != None:
            primary.terminalString.accept(self,primary.terminalString)
        elif primary.empty != None:
            primary.empty.accept(self,primary.empty)

    def visitIdentifier(self,identifier):
        if (self.first==None): self.first=identifier.value.capitalize()
        self.to_generate.append((identifier.value.capitalize(),0))
