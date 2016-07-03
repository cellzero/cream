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
	
