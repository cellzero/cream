import os
from OpenGL.GL import *
from texture import load_texture
SIZE_OF_FLOAT = 4

class Object:
    def __init__(self, path):
        self.mtl = {}
        self.group = {}
        self.load_obj(path)
        self.texture_ids = []
        self.vertex_buffer_ids = []
        self.uv_buffer_ids = []
        self.normal_buffer_ids = []
        self.vao_ids = []
        self.texture_ids = []
        self.mtl_buffer_list = []
        self.geom_nums = []

    def bind_buffer(self):
        for (_, group) in self.group.items():
            vertex_buffer_data = group.vertices
            uv_buffer_data = group.uvs
            normals_buffer_data = group.normals

            # VAO
            vertex_array_id = glGenVertexArrays(1)
            glBindVertexArray(vertex_array_id)
            self.vao_ids.append(vertex_array_id)

            # texture
            self.texture_ids.append(group.mtl.map_Kd_id)

            # mtl
            self.mtl_buffer_list.append(group.mtl)

            # VBO
            # vertex
            vertex_buffer_id = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
            vertex_buffer = (GLfloat * len(vertex_buffer_data))(*vertex_buffer_data)
            glBufferData(GL_ARRAY_BUFFER, len(vertex_buffer_data) * SIZE_OF_FLOAT,
                         vertex_buffer, GL_STATIC_DRAW)
            self.vertex_buffer_ids.append(vertex_buffer_id)
            # UV
            uv_buffer_id = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, uv_buffer_id)
            uv_buffer = (GLfloat * len(uv_buffer_data))(*uv_buffer_data)
            glBufferData(GL_ARRAY_BUFFER, len(uv_buffer_data) * SIZE_OF_FLOAT,
                         uv_buffer, GL_STATIC_DRAW)
            self.uv_buffer_ids.append(uv_buffer_id)
            # normal
            normal_buffer_id = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, normal_buffer_id)
            normal_buffer = (GLfloat * len(normals_buffer_data))(*normals_buffer_data)
            glBufferData(GL_ARRAY_BUFFER, len(normals_buffer_data) * SIZE_OF_FLOAT,
                         normal_buffer, GL_STATIC_DRAW)
            self.normal_buffer_ids.append(normal_buffer_id)
            # number of geometry
            geom_num = int(len(vertex_buffer_data) / 3)
            self.geom_nums.append(geom_num)
            # g_face_type.append(group.face_type)

            # unbind
            glBindVertexArray(0)


    def load_obj(self, path):
        tmp_vs = []
        tmp_vts = []
        tmp_vns = []
        tmp_g = None
        f_obj = open(path, 'r')
        for line in f_obj.readlines():
            if len(line) <= 1 or line[0] == '#':
                continue
            line = line.strip()
            name, params = line.split(' ', 1)
            params = params.strip().split(' ')
            if name == 'mtllib':
                p = os.path.split(path)[0]
                f = params[0]
                self.load_mtl(os.path.join(p, f))
            elif name == 'v':
                tmp_vs.append((float(params[0]), float(params[1]), float(params[2])))
            elif name == 'vn':
                tmp_vns.append((float(params[0]), float(params[1]), float(params[2])))
            elif name == 'vt':
                tmp_vts.append((float(params[0]), float(params[1]), float(params[2])))
            elif name == 'g':
                tmp_g = Group()
                self.group[params[0]] = tmp_g
            elif name == 'usemtl':
                tmp_mtl = self.mtl[params[0]]
                tmp_g.mtl = tmp_mtl
            elif name == 'f':
                vertex_count = 0
                for f in params:
                    if len(f) <= 0:
                        continue
                    vertex_count += 1
                    # 顶点，纹理，法向量
                    v, t, n = f.split('/')
                    tmp_g.vertices.extend(tmp_vs[int(v) - 1])
                    tmp_g.uvs.extend(tmp_vts[int(t) - 1])
                    tmp_g.normals.extend(tmp_vns[int(n) - 1])
                # face type
                if vertex_count == 3:
                    tmp_g.face_type = GL_TRIANGLES
                elif vertex_count == 4:
                    tmp_g.face_type = GL_QUADS
        f_obj.close()

    def load_mtl(self, path):
        f_mtl = open(path, 'r')
        for line in f_mtl.readlines():
            line = line.strip()
            if len(line) <= 0 or line[0] == '#':    # commit
                continue
            name, params = line.split(' ', 1)
            params = params.strip().split(' ')
            if name == 'newmtl':
                m = Material()
                self.mtl[params[0]] = m
            elif name == 'Ns':
                m.Ns = float(params[0])
            elif line.find('Ni') == 0:
                m.Ni = float(params[0])
            elif line.find('d') == 0:
                m.d = float(params[0])
            elif line.find('Tr') == 0:
                m.Tr = float(params[0])
            elif line.find('Tf') == 0:
                m.Tf[0] = float(params[0])
                m.Tf[1] = float(params[1])
                m.Tf[2] = float(params[2])
            elif line.find('illum') == 0:
                m.illum = int(float(params[0]))
            elif line.find('Ka') == 0:
                m.Ka[0] = float(params[0])
                m.Ka[1] = float(params[1])
                m.Ka[2] = float(params[2])
            elif line.find('Kd') == 0:
                m.Kd[0] = float(params[0])
                m.Kd[1] = float(params[1])
                m.Kd[2] = float(params[2])
            elif line.find('Ks') == 0:
                m.Ks[0] = float(params[0])
                m.Ks[1] = float(params[1])
                m.Ks[2] = float(params[2])
            elif line.find('Ke') == 0:
                m.Ke[0] = float(params[0])
                m.Ke[1] = float(params[1])
                m.Ke[2] = float(params[2])
            elif line.find('map_Ka') == 0:
                m.map_Ka_str = params[0]
                p = os.path.split(path)[0]
                m.map_Ka_id = load_texture(os.path.join(p, m.map_Ka_str))
            elif line.find('map_Kd') == 0:
                m.map_Kd_str = params[0]
                p = os.path.split(path)[0]
                m.map_Kd_id = load_texture(os.path.join(p, m.map_Kd_str))
        f_mtl.close()


class Group:
    def __init__(self):
        self.mtl = None
        self.vertices = []
        self.uvs = []
        self.normals = []
        self.face_type = GL_TRIANGLES


class Material:
    def __init__(self):
        self.Ns = 0.0  # 反射指数值，数值越高高光越密，一般取值0-1000
        self.Ni = 0.0  # 折射值，材质表面的光密度
        self.d = 0.0  # 渐隐指数，融入背景的程度
        self.Tr = 0.0  # TODO
        self.Tf = [0.0, 0.0, 0.0]  # 滤光透射率
        self.illum = 0  # 照明模型枚举
        ("0. 色彩开，阴影色关\n"
         " 1. 色彩开，阴影色开\n"
         " 2. 高光开\n"
         " 3. 反射开，光线追踪开\n"
         " 4. 透明： 玻璃开 反射：光线追踪开\n"
         " 5. 反射：菲涅尔衍射开，光线追踪开\n"
         " 6. 透明：折射开 反射：菲涅尔衍射关，光线追踪开\n"
         " 7. 透明：折射开 反射：菲涅尔衍射开，光线追踪开\n"
         " 8. 反射开，光线追踪关\n"
         " 9. 透明： 玻璃开 反射：光线追踪关\n"
         " 10. 投射阴影于不可见表面")
        self.Ka = [0.0, 0.0, 0.0]  # 环境反射
        self.Kd = [0.0, 0.0, 0.0]  # 漫反射
        self.Ks = [0.0, 0.0, 0.0]  # 镜面反射
        self.Ke = [0.0, 0.0, 0.0]  # TODO
        self.map_Ka_str = ''  # 阴影色纹理贴图
        self.map_Kd_str = ''  # 固有色纹理贴图
        self.map_Ka_id = 0
        self.map_Kd_id = 0


m_empty = Material()
