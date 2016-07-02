#coding=utf-8

from Texture import Texture as Texture

class LoaderMTL:
	def __init__( self ):
		self.cache = {}
		self.mtl = None
		self.mtlname = ''
	
	def load( self, filename ):
		fi = open( filename )
		mtltable = {}
		for line in fi:
			# 空行
			if len(line) <= 0 or line[0] == '\n':
				continue
			# 行首注释
			if line[0] == '#':
				continue
			strs = line.strip().split(' ')
			label, values = strs[0], strs[1:]
			if label == 'newmtl':
				self.mtlname = values[0]
				self.mtl = Texture()
				mtltable[self.mtlname] = self.mtl
			else:
				self.mtl.set( label, values )
		if len( mtltable ) > 0:
			self.cache[filename] = mtltable
		fi.close()
	
	def getTexture( self, filename, mtlname ):
		try:
			texture = self.cache[filename][mtlname]
			return texture
		except KeyError:
			return None

if __name__ == '__main__':
	print('hello')
	loader = LoaderMTL()
	loader.load('../../resources/box.mtl')
	texture = loader.getTexture('../../resources/box.mtl', 'wire_135059008')
	print('Ka', texture.Ka)
	print('Tr', texture.Tr)