from OpenGL.GL import *
from OpenGL.GLUT import *
from shader import BaseShaderProgram
from object import Object
import os
import sys
import numpy as np
from matrix_transform import *
from math import exp, modf,pi

WIDTH = 640
HEIGHT = 480
FPS = 50
ESC = b'\033'
SIZE_OF_FLOAT = 4

window = 0
vertex_array_id = 0
vertex_buffer_id = 0
uv_buffer_id = 0
texture_id = 0
program_id = 0

# uniform variables
uniform_loc = {}
uniforms = ['myTextureSampler',b"MVP"]

# motion control
rotating = False
scaling = False
(x0,y0)=(0,0)

verticalAngle = 0
horizontalAngle = 0
scale_ratio = 1


# transform matrix
ProjectionMatrix = np.identity(4,dtype=np.float32)
ModelMatrix = np.identity(4,dtype=np.float32)
ViewMatrix = np.identity(4,dtype=np.float32)
TranslationMatrix = np.identity(4,dtype=np.float32)
ScalingMatrix = np.identity(4,dtype=np.float32)

def reshape(w, h):
    """TODO"""
    glViewport(0, 0, w, h)


def display():
    global vertex_buffer_id,uv_buffer_id,horizontalAngle,verticalAngle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	
    glUseProgram(program_id)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glUniform1i(uniform_loc['myTextureSampler'], 0)

    # set transform matrix
    ModelMatrix = np.identity(4,'f')
    ModelMatrix = rotate(ModelMatrix,verticalAngle,np.array([1,0,0],'f'))
    ModelMatrix = rotate(ModelMatrix.T,horizontalAngle,np.array([0,1,0],'f'))
    ModelMatrix = dots(ModelMatrix,scale(scale_ratio,scale_ratio,scale_ratio))
    ProjectionMatrix = perspective(45,4/3,0.1,100)
    ViewMatrix = lookAt(
        np.array([0,0,3]),
        np.array([0,0,0]),
        np.array([0,1,0])
    )
    # MVP = np.dot(np.dot(ProjectionMatrix.T,ViewMatrix.T),ModelMatrix.T).T
    MVP = dots(ProjectionMatrix,ViewMatrix,ModelMatrix)
    glUniformMatrix4fv(uniform_loc[b"MVP"], 1, GL_TRUE,c_matrix(MVP))

    # vertex
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    # uv
    glEnableVertexAttribArray(1)
    glBindBuffer(GL_ARRAY_BUFFER, uv_buffer_id)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    # draw
    glDrawArrays(GL_TRIANGLES, 0, 12 * 3)

    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glutSwapBuffers()


def keyboard(key, x, y):
    global window
    if key == ESC:
        glutDestroyWindow(window)
        sys.exit(0)


def mouse(button, state, x, y):
    global rotating, scaling, x0, y0
    if button == GLUT_LEFT_BUTTON:
        rotating = (state == GLUT_DOWN)
    elif button == GLUT_RIGHT_BUTTON:
        scaling = (state == GLUT_DOWN)
    x0, y0 = x, y


def update(val):
    if val == 1:
        glutPostRedisplay()
        # glutTimerFunc(int(1000 / FPS), update, 1)

def screen2space(x, y):
    global scale_ratio
    width, height = glutGet(GLUT_WINDOW_WIDTH),glutGet(GLUT_WINDOW_HEIGHT)
    radius = min(width, height)*scale_ratio
    return (2.*x-width)/radius, -(2.*y-height)/radius

def motion(x1, y1):
    global x0, y0, scale_ratio,WIDTH,HEIGHT,horizontalAngle,verticalAngle
    delta_unit_x = 360.0 / WIDTH * pi / 180.0
    delta_unit_y = 360.0 / HEIGHT * pi / 180.0
    if rotating:
        horizontalAngle -= delta_unit_x * (x1 - x0)
        verticalAngle += delta_unit_y * (y1 - y0)
        verticalAngle = numpy.clip(verticalAngle, -pi / 2, pi / 2)
    if scaling:
        scale_ratio *= exp(((x1 - x0) - (y1 - y0)) * .01)
    x0, y0 = x1, y1
    glutPostRedisplay()



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
        # 'shaders/v_simple_texture.glsl', 'shaders/f_simple_texture.glsl').program_id
        'shaders/Transform.vs.glsl', 'shaders/f_green.glsl').program_id

    for uniform in uniforms:
        uniform_loc[uniform] = glGetUniformLocation(program_id, uniform)


def init_object():
    """load object data"""
    global texture_id, vertex_array_id, vertex_buffer_id, uv_buffer_id
    # read obj file
    tmp_obj = Object(os.path.join('..', 'resources', 'box.obj'))
    vertex_buffer_data = []
    uv_buffer_data = []
    for (_, group) in tmp_obj.group.items():
        texture_id = group.mtl.map_Kd_id
        vertex_buffer_data.extend(group.vertices)
        uv_buffer_data.extend(group.uvs)
    # VAO
    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    # VBO
    # vertex
    vertex_buffer_id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
    vertex_buffer = (GLfloat * len(vertex_buffer_data))(*vertex_buffer_data)
    glBufferData(GL_ARRAY_BUFFER, len(vertex_buffer_data) * SIZE_OF_FLOAT,
                 vertex_buffer, GL_STATIC_DRAW)
    # UV
    uv_buffer_id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, uv_buffer_id)
    uv_buffer = (GLfloat * len(uv_buffer_data))(*uv_buffer_data)
    glBufferData(GL_ARRAY_BUFFER, len(uv_buffer_data) * SIZE_OF_FLOAT,
                 uv_buffer, GL_STATIC_DRAW)



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
