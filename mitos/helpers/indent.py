# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


class Indent(object):
    '''
    An indentator simplifying information display with automated tabulations
    '''
    INDENT = 2

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.indentation = None

    def indent(self, text):

        if self.indentation is None:
            self.indentation = -self.INDENT
        self.indentation += self.INDENT
        self.say(text)

    def dedent(self):
        self.indentation -= self.INDENT

    def say(self, text):
        output = ''
        if (self.indentation > 0):
            for i in range(1, self.indentation):
                output += ' '
        output += text
        if self.verbose:
            print(output)
