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

    def __repr__(self):
        '''
        Print format of the object : Grammar - Grammar.syntax
        '''
        return "Grammar - {0}".format(str(self.syntax))

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

    def __repr__(self):
        '''
        Print format of the object :
        Syntax -
            Syntax.syntaxRules[0]
            Syntax.syntaxRules[1]
            ...
        '''
        string = "Syntax - "
        for syntaxRule in self.syntaxRules:
            string += '\n\t' + str(syntaxRule)
        return string

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

    def __repr__(self):
        '''
        Print format of the object :
        Syntax Rule - SyntaxRule.identifier
        '''
        string = "Syntax Rule - {0} = ".format(self.identifier)
        string += '\n\t- ' + str(self.definitions)
        return string

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

    def __repr__(self):
        string = "Definitions - "
        for definition in self.definitions:
            string += '\n\t' + str(definition)
        return string

class Definition(Node):
    '''
    A definition (a set of terms)
    Definition = Term, {',', Term};  //EBNF
    '''
    def __init__(self,terms=[]):
        self.terms = []

    def addTerm(self,term):
        self.terms.append(term)

    def __repr__(self):
        string = "Definition - "
        for term in self.terms:
            string += '\n\t\t' + str(term)
        return string


class Term(Node):
    '''
    A term (Factor & Exception)
    Term = Factor, ['-', Exception];  //EBNF
    '''
    def __init__(self,factor=None,exception=None):
        self.factor    = factor
        self.exception = exception

    def __repr__(self):
         string = "Term - {0}".format(self.factor)
         if self.exception != None:
             string += ' - {0}'.format(self.exception)
         return string

class Exception(Node):
    '''
    An exception
    Exception = Factor;  //EBNF
    '''
    def __init__(self,factor=None):
        self.factor = factor

    # def __repr__(self):
    #     return "Exception - {0}".format(self.factor)

class Factor(Node):
    '''
    A factor
    Factor = [Integer, '*'], Primary; //EBNF
    '''
    def __init__(self,integer=0,primary=None):
        self.integer = integer
        self.primary = primary

    def __repr__(self):
        string = "Factor - "
        if self.integer != 0:
            string += str(integer) + " * "
        string += str(self.primary)
        return string

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

    def __repr__(self):
        string = 'Primary - '
        if self.optionalSeq != None:
            string += str(self.optionalSeq)
        elif self.identifier != None:
            string += str(self.identifier)
        elif self.repeatedSeq != None:
            string += str(self.repeatedSeq)
        elif self.groupedSeq != None:
            string += str(self.groupedSeq)
        elif self.specialSeq != None:
            string += str(self.specialSeq)
        elif self.terminalString != None:
            string += str(self.terminalString)
        elif self.empty != None:
            string += str(self.empty)
        return string


class OptionalSeq(Node):
    '''
    An optional sequence:
    OptionalSeq = '[', Definitions, ']';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def __repr__(self):
        string = "Optional Sequence - [ "
        for definition in self.definitions.definitions:
            string += str(definition)
        string += "]"
        return string

class RepeatedSeq(Node):
    '''
    A repeated sequence:
    RepeatedSeq = '{', Definitions, '}';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def __repr__(self):
        string = "Repeated Sequence - { "
        string += str(self.definitions)
        string += "}"
        return string

class GroupedSeq(Node):
    '''
    A grouped sequence
    GroupedSeq = '(', Definitions, ')';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def __repr__(self):
        string = "Grouped Sequence - ( "
        string += str(self.definitions)
        string += ")"
        return string

class SpecialSeq(Node):
    '''
    A special Sequence
    SpecialSeq = '?', {Character - '?'}, '?';  //EBNF
    '''
    def __init__(self,value=''):
        self.value = value

    def __repr__(self):
        return "Special Sequence - ? {0} ?".format(self.value)

class TerminalString(Node):
    def __init__(self,value=''):
        self.value = value

    def __repr__(self):
        return "Terminal String - {0}".format(self.value)

class TerminalStringSQuote(TerminalString):
    '''
    A terminal string with simple quotes
    TerminalString = "'", Character - "'", {Character - "'"}, "'" //EBNF
    '''
    def __init__(self,value=''):
        super().__init__(value)
        self.separator = '\''

    def __repr__(self):
        return "Terminal String (S Quote) - {0}".format(self.value)

class TerminalStringDQuote(TerminalString):
    '''
    A terminal string with double quotes
    TerminalString = '"', Character - '"', {Character - '"'}, '"' //EBNF
    '''
    def __init__(self,value=''):
        super().__init__(value)
        self.separator = '\"'

    def __repr__(self):
        return "Terminal String (D Quote) - {0}".format(self.value)

class Identifier(Node):
    '''
    An identifier
    Identifier = Letter, {Letter | Digit};  //EBNF
    --> Simplified with a value only here
    '''
    def __init__(self,value=''):
        self.value = value

    def __repr__(self):
        return "Identifier: '{0}' ".format(self.value)

class Empty(Node):
    '''
    An empty primary
    Empty = ;  //EBNF
    '''
    def __init__(self):
        pass

    def __repr__(self):
        return "Empty Primary"

class Integer(Node):
    '''
    An integer
    Integer = Digit, {Digit};  //EBNF
     --> Simplified with a value only here
    '''
    def __init__(self,value=0):
        self.value = value

    def __repr__(self):
        return "Integer - {0}".format(self.value)
