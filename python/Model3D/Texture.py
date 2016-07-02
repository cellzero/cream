#coding=utf-8

#===================================================
# 记录表面材质，如：折射、反射系数等。
# 目前不考虑贴图。 
#===================================================

class Texture:
	
	
	def __init__( self ):
		# 光照反射系数，对应数据为(r, g, b, a)
		self.Ka = [ 1.0, 1.0, 1.0, 1.0 ]	# ambient 环境光
		self.Kd = [ 0.0, 0.0, 0.0, 1.0 ]	# diffuse 散射光
		self.Ks = [ 0.0, 0.0, 0.0, 1.0 ]	# specular 镜面光
		self.Ke = [ 0.0, 0.0, 0.0, 1.0 ]	# emissive 放射光
		# 发光体属性
		self.Ns = 0	# shininess 光亮度
		self.Ni = 0	# optical density 光密度
		# alpha 透明属性
		self.d = 1
		self.Tr = 0
		# 反光程度
		self.sharpness = 2	# sharpness 锐度
		self.illum = 2		# illumination 照明度
		# 透射滤波，对应数据为(r, g, b, a)
		self.Tf = [ 1.0, 1.0, 1.0, 1.0 ]
	
	def set( self, key, values ):
		self.param_dict.get(key)( self, values )
	
	def setNs( self, values ):
		self.Ns = int(values[0])
	
	def setD( self, values ):
		self.D = int(values[0])
	
	def setTr( self, values ):
		self.Tr = int(values[0])
		
	def setIllum( self, values ):
		self.illum = int(values[0])
	
	def setRGBA( self, param, values ):
		param[0] = float(values[0])
		param[1] = float(values[1])
		param[2] = float(values[2])
		param[3] = float(values[3]) if len(values) > 3 else 1.0
	
	def setTf( self, values ):
		self.setRGBA( self.Tf, values )
	
	def setKa( self, values ):
		self.setRGBA( self.Ka, values )
	
	def setKd( self, values ):
		self.setRGBA( self.Kd, values )
	
	def setKs( self, values ):
		self.setRGBA( self.Ks, values )
	
	# 参数名称字典
	param_dict = { 'Ns' : setNs, 'd' : setD, 
		'Tr' : setTr, 'Tf' : setTf, 'illum' : setIllum, 
		'Ka' : setKa, 'Kd' : setKd, 'Ks' : setKs
	}
