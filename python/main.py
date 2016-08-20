from OpenGL.GL import *
from OpenGL.GLUT import *
from shader import BaseShaderProgram
from object import Object
import os
import sys
import numpy as np
from matrix_transform import *

WIDTH = 640
HEIGHT = 480
FPS = 50
ESC = b'\033'
SIZE_OF_FLOAT = 4

window = 0
vertex_array_id = 0
g_vertex_buffer_id = []
g_uv_buffer_id = []
g_texture_id = []
program_id = 0
g_geom_num = []
g_face_type = []

# uniform variables
uniform_loc = {}
uniforms = ['myTextureSampler', b"MVP"]
g_vertex_buffer_data = [
    -1.0, -1.0, 0.0,
    1.0, -1.0, 0.0,
    0.0, 1.0, 0.0
]

# transform matrix
ProjectionMatrix = np.identity(4, dtype=np.float32)
ModelMatrix = np.identity(4, dtype=np.float32)
ViewMatrix = np.identity(4, dtype=np.float32)


def reshape(w, h):
    """TODO"""
    glViewport(0, 0, w, h)


def display():
    global g_vertex_buffer_id, g_uv_buffer_id
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(program_id)
    # set transform matrix
    matrix_scale = scale(0.05)
    ModelMatrix = np.dot(matrix_scale, np.identity(4, 'f'))
    ProjectionMatrix = perspective(45, 4 / 3, 0.1, 100)
    ViewMatrix = lookAt(
        np.array([1, 1, -1]),
        np.array([0, 0, 0]),
        np.array([0, 1, 0])
    )
    MVP = np.dot(np.dot(ProjectionMatrix.T, ViewMatrix.T), ModelMatrix).T
    # MVP = np.dot(ProjectionMatrix.T, ViewMatrix.T).T
    glUniformMatrix4fv(uniform_loc[b"MVP"], 1, GL_FALSE, c_matrix(MVP))

    # display
    for i in range(len(g_geom_num)):
        # texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, g_texture_id[i])
        glUniform1i(uniform_loc['myTextureSampler'], 0)
        # vertex
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, g_vertex_buffer_id[i])
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        # uv
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, g_uv_buffer_id[i])
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        # draw
        glDrawArrays(g_face_type[i], 0, g_geom_num[i] * 4)
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

    # swap buffer
    glutSwapBuffers()


def keyboard(key, x, y):
    global window
    if key == ESC:
        glutDestroyWindow(window)
        sys.exit(0)


def mouse(button, state, x, y):
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
            print('left button', x, y)


def update(val):
    if val == 1:
        glutPostRedisplay()
        # glutTimerFunc(int(1000 / FPS), update, 1)


def motion(x1, y1):
    # print(x1," ",y1)
    pass


def init_opengl():
    """set opengl parameter"""
    # depth test
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    glClearColor(0.0, 0.0, 0.4, 0.0)


def init_texture():
    pass


def init_glut(argv):
    """glut initialization."""
    global window
    glutInit(argv)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    window = glutCreateWindow(b'tutorial 02')

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutTimerFunc(int(1000 / FPS), update, 1)


def init_shader():
    """load shader and set initial value"""
    global program_id, uniforms, uniform_loc
    program_id = BaseShaderProgram(
        'shaders/v_simple_texture.glsl', 'shaders/f_simple_texture.glsl').program_id
        # 'shaders/Transform.vs.glsl', 'shaders/f_green.glsl').program_id

    for uniform in uniforms:
        uniform_loc[uniform] = glGetUniformLocation(program_id, uniform)


def init_object():
    """load object data"""
    global g_texture_id, vertex_array_id, g_vertex_buffer_id, g_uv_buffer_id, g_geom_num
    # read obj file
    tmp_obj = Object(os.path.join('..', 'resources', 'flower3d.obj'))
    # bind
    # VAO
    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    for (_, group) in tmp_obj.group.items():
        g_texture_id.append(group.mtl.map_Kd_id)
        vertex_buffer_data = group.vertices
        uv_buffer_data = group.uvs
        # VBO
        # vertex
        vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        vertex_buffer = (GLfloat * len(vertex_buffer_data))(*vertex_buffer_data)
        glBufferData(GL_ARRAY_BUFFER, len(vertex_buffer_data) * SIZE_OF_FLOAT,
                     vertex_buffer, GL_STATIC_DRAW)
        g_vertex_buffer_id.append(vertex_buffer_id)
        # UV
        uv_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, uv_buffer_id)
        uv_buffer = (GLfloat * len(uv_buffer_data))(*uv_buffer_data)
        glBufferData(GL_ARRAY_BUFFER, len(uv_buffer_data) * SIZE_OF_FLOAT,
                     uv_buffer, GL_STATIC_DRAW)
        g_uv_buffer_id.append(uv_buffer_id)
        # number of geometry
        geom_num = int(len(vertex_buffer_data) / 4)
        g_geom_num.append(geom_num)
        g_face_type.append(group.face_type)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    init_glut(argv)
    init_opengl()
    init_shader()
    init_texture()
    init_object()
    glutMainLoop()


main()
