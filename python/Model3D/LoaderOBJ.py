#coding=utf-8
import MtlLoader

class ObjLoader:
	def __init__(self):
		self.cache = {}
	
	def load( self, path ):
		try:
			
