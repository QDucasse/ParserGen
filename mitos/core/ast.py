# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


from abc import ABC

class Node(ABC):
    '''
    Principal Node of the system, meta-defines the accept function for all others subnodes.
    '''
    def accept(self, visitor, args):
        '''
        Accepts the upcoming visitor with its arguments.

        Parameters
        ----------
        visitor: Visitor object.
            Visitor of the ast.

        args: objects
            Arguments that need to be passed to the visit___ method cast on the
            visitor.

        Note
        ----
        The accept function, as described in the Visitor pattern, allows the receiver
        (subnode) to cast the correct visitor visit method.
        '''
        # Formatting the name
        className  = self.__class__.__name__
        methodName = getattr(visitor, "visit" + className)
        # Casting the visit<className> method on the visitor
        methodName(args)

class Grammar(Node):
    '''
    Our equivalent to other languages "Program", starting point for the parsing operation.
    Parameters
    ----------
    syntax: Syntax object
        The syntax of our grammar. Default None
    '''
    def __init__(self,syntax=None):
        self.syntax = syntax

class Syntax(Node):
    '''
    A set of syntax rules.
    Syntax = SyntaxRule, {SyntaxRule}; //EBNF

    Parameters
    ----------
    syntaxRules: SyntaxRule list
        List of the syntax rules contained within the syntax.
    '''
    def __init__(self,syntaxRules=[]):
        self.syntaxRules = syntaxRules

    def addRule(self, syntaxRule):
        '''
        Simple append to the syntaxRules instance variable.
        '''
        self.syntaxRules.append(syntaxRule)

class SyntaxRule(Node):
    '''
    A syntax rule.
    SyntaxRule = Identifier, '=', Definitions, ';';  //EBNF

    Parameters
    ----------
    identifier: Identifier object
        Name of the syntax rule.

    definitions: Definition list
        List of definitions contained in the syntax rule.
    '''
    def __init__(self,identifier=None,definitions=None):
        self.identifier  = identifier
        self.definitions = definitions

class Definitions(Node):
    ##### TODO : SAME AS SYNTAX RULE, NO NEED FOR DEFINITIONS
    ############# OR NEED FOR SYNTAX RULES
    '''
    A set of definitions
    Definitions = Definition, {'|', Definition};  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def addDefinition(self,definition):
        self.definitions.append(definition)

class Definition(Node):
    '''
    A definition (a set of terms)
    Definition = Term, {',', Term};  //EBNF
    '''
    def __init__(self,terms=[]):
        self.terms = []

    def addTerm(self,term):
        self.terms.append(term)

class Term(Node):
    '''
    A term (Factor & Exception)
    Term = Factor, ['-', Exception];  //EBNF
    '''
    def __init__(self,factor=None,exception=None):
        self.factor    = factor
        self.exception = exception

class Exception(Node):
    '''
    An exception
    Exception = Factor;  //EBNF
    '''
    def __init__(self,factor=None):
        self.factor = factor

class Factor(Node):
    '''
    A factor
    Factor = [Integer, '*'], Primary; //EBNF
    '''
    def __init__(self,integer=0,primary=None):
        self.integer = integer
        self.primary = primary

class Primary(Node):
    '''
    A primary corresponding to either of those sequence:
    Primary = OptionalSeq
            | RepeatedSeq
            | GroupedSeq
            | SpecialSeq
            | TerminalString
            | Identifier
            | Empty;            //EBNF
    '''
    def __init__(self,optionalSeq    = None,
                      repeatedSeq    = None,
                      groupedSeq     = None,
                      specialSeq     = None,
                      terminalString = None,
                      identifier     = None,
                      empty          = None):
        self.optionalSeq    = optionalSeq
        self.repeatedSeq    = repeatedSeq
        self.groupedSeq     = groupedSeq
        self.specialSeq     = specialSeq
        self.terminalString = terminalString
        self.identifier     = identifier
        self.empty          = empty

class OptionalSeq(Node):
    '''
    An optional sequence:
    OptionalSeq = '[', Definitions, ']';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

class RepeatedSeq(Node):
    '''
    A repeated sequence:
    RepeatedSeq = '{', Definitions, '}';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

class GroupedSeq(Node):
    '''
    A grouped sequence
    GroupedSeq = '(', Definitions, ')';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

class SpecialSeq(Node):
    '''
    A special Sequence
    SpecialSeq = '?', {Character - '?'}, '?';  //EBNF
    '''
    def __init__(self,value=''):
        self.value = value

class TerminalString(Node):
    def __init__(self,value=''):
        self.value = value

class TerminalStringSQuote(TerminalString):
    '''
    A terminal string with simple quotes
    TerminalString = "'", Character - "'", {Character - "'"}, "'" //EBNF
    '''
    def __init__(self,value=''):
        super().__init__(value)
        self.separator = '\''

class TerminalStringDQuote(TerminalString):
    '''
    A terminal string with double quotes
    TerminalString = '"', Character - '"', {Character - '"'}, '"' //EBNF
    '''
    def __init__(self,value=''):
        super().__init__(value)
        self.separator = '\"'

class Identifier(Node):
    '''
    An identifier
    Identifier = Letter, {Letter | Digit};  //EBNF
    --> Simplified with a value only here
    '''
    def __init__(self,value=''):
        self.value = value

class Empty(Node):
    '''
    An empty primary
    Empty = ;  //EBNF
    '''
    def __init__(self):
        pass

class Integer(Node):
    '''
    An integer
    Integer = Digit, {Digit};  //EBNF
     --> Simplified with a value only here
    '''
    def __init__(self,value=0):
        self.value = value
