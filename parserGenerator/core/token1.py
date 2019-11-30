# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


class Token:
	'''
	Our token definition:
	lexem (kind and value) + position in the program raw text
	'''
	def __init__(self, kind, value, position):
		self.kind = kind
		self.value = value
		self.position = position

	def __repr__(self):
		return self.kind
