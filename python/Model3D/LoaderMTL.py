#coding=utf-8

from Texture import Texture as Texture

class LoaderMTL:
	def __init__( self ):
		self.cache = {}
	
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
				mtlname = values[0]
				mtl = Texture()
				mtltable[mtlname] = mtl
			else:
				self.set( mtl, label, values )
		if len( mtltable ) > 0:
			self.cache[filename] = mtltable
		fi.close()
	
	def getTexture( self, filename, mtlname ):
		try:
			texture = self.cache[filename][mtlname]
			return texture
		except KeyError:
			return None
	
	def set( self, mtl, key, values ):
		self.param_dict.get(key)( mtl, values )
	
	def set_Ns( mtl, values ):
		mtl.Ns = int(values[0])
	
	def set_d( mtl, values ):
		mtl.d = int(values[0])
	
	def set_Tr( mtl, values ):
		mtl.Tr = int(values[0])
		
	def set_illum( mtl, values ):
		mtl.illum = int(values[0])
	
	def set_4f( param, values ):
		param[0] = float(values[0])
		param[1] = float(values[1])
		param[2] = float(values[2])
		param[3] = float(values[3]) if len(values) > 3 else 1.0
	
	def set_Tf( mtl, values ):
		LoaderMTL.setRGBA( mtl.Tf, values )
	
	def set_Ka( mtl, values ):
		LoaderMTL.setRGBA( mtl.Ka, values )
	
	def set_Kd( mtl, values ):
		LoaderMTL.setRGBA( mtl.Kd, values )
	
	def set_Ks( mtl, values ):
		LoaderMTL.setRGBA( mtl.Ks, values )
	
	# 参数名称字典
	param_dict = { 'Ns' : set_Ns, 'd' : set_d, 
		'Tr' : set_Tr, 'Tf' : set_Tf, 'illum' : set_illum, 
		'Ka' : set_Ka, 'Kd' : set_Kd, 'Ks' : set_Ks
	}
	setRGBA = set_4f

if __name__ == '__main__':
	print('hello')
	loader = LoaderMTL()
	loader.load('../../resources/box.mtl')
	texture = loader.getTexture('../../resources/box.mtl', 'wire_135059008')
	print('Ka', texture.Ka)
	print('Tr', texture.Tr)