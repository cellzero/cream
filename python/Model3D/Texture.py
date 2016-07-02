#coding=utf-8

#===================================================
# ��¼������ʣ��磺���䡢����ϵ���ȡ�
# Ŀǰ��������ͼ�� 
#===================================================

class Texture:
	
	
	def __init__( self ):
		# ���շ���ϵ������Ӧ����Ϊ(r, g, b, a)
		self.Ka = [ 1.0, 1.0, 1.0, 1.0 ]	# ambient ������
		self.Kd = [ 0.0, 0.0, 0.0, 1.0 ]	# diffuse ɢ���
		self.Ks = [ 0.0, 0.0, 0.0, 1.0 ]	# specular �����
		self.Ke = [ 0.0, 0.0, 0.0, 1.0 ]	# emissive �����
		# ����������
		self.Ns = 0	# shininess ������
		self.Ni = 0	# optical density ���ܶ�
		# alpha ͸������
		self.d = 1
		self.Tr = 0
		# ����̶�
		self.sharpness = 2	# sharpness ���
		self.illum = 2		# illumination ������
		# ͸���˲�����Ӧ����Ϊ(r, g, b, a)
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
	
	# ���������ֵ�
	param_dict = { 'Ns' : setNs, 'd' : setD, 
		'Tr' : setTr, 'Tf' : setTf, 'illum' : setIllum, 
		'Ka' : setKa, 'Kd' : setKd, 'Ks' : setKs
	}
