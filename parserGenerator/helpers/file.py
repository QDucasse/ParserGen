# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


class File():
    '''
    File handler managing opening, writing and closing
    '''
    def __init__(self,name):
        self.f=open(name,"w")

    def write(self,data):
        self.f.write(data)

    def close(self):
        self.f.close()
