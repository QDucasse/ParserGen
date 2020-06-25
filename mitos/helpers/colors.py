# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


class Colors(object):
    '''
    Classic colors that can be used to display more pleasantly information
    in the terminal
    ex: Colors.OKGREEN + 'Text in Green!' +  Colors.ENDC
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
