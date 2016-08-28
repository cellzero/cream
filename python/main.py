from OpenGL.GL import *
from OpenGL.GLUT import *
from shader import BaseShaderProgram
from object import Object
import os
import sys
import numpy as np
from matrix_transform import *
from math import pi, radians
from Camera import Camera

WIDTH = 800
HEIGHT = 600
FPS = 50
ESC = b'\033'
SIZE_OF_FLOAT = 4

window = 0
program_id = 0

# uniform variables
uniform_loc = {}
uniforms = ['myTextureSampler',
            'MVP', 'M', 'V', 'NormalMatrix',
            'lightPos_worldspace',
            'material.ambient',
            'material.diffuse',
            'material.specular',
            'material.shininess',
            ]

# motion control
g_camera = Camera()

lightPos_worldspace = np.array([0, 0, 3])

#Objects
boxObj = None
flowerObj = None
g_object_list = []


def reshape(w, h):
    """TODO"""
    glViewport(0, 0, w, h)


def display():
    global lightPos_worldspace, g_camera
    global boxObj, flowerObj
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(program_id)
    # set transform matrix
    # matrix_scale = scale(g_scale_ratio)
    # ModelMatrix = rotate(matrix_scale.T, g_verticalAngle, np.array([1, 0, 0], 'f'))
    # ModelMatrix = rotate(ModelMatrix.T, g_horizontalAngle, np.array([0, 1, 0], 'f'))
    # matrix_translate = translate(g_translate_x, g_translate_y, 0.0)
    # ModelMatrix = np.dot(matrix_translate, ModelMatrix)

    ProjectionMatrix = perspective(radians(g_camera.zoom), 4 / 3, 0.1, 100)
    ViewMatrix = g_camera.getViewMatrix()
    glUniformMatrix4fv(uniform_loc['V'], 1, GL_TRUE, c_matrix(ViewMatrix))

    # set light parameter
    lightPos = g_camera.getLightPosition()
    glUniform3f(uniform_loc['lightPos_worldspace'], lightPos[0], lightPos[1], lightPos[2])
    glUniform1f(uniform_loc['material.shininess'], 32)

    # display
    obj = boxObj
    ModelMatrix = np.identity(4, 'f')
    matrix_translate = translate(2, 0, -5)
    ModelMatrix = dots(matrix_translate, ModelMatrix)
    MVP = dots(ProjectionMatrix, ViewMatrix, ModelMatrix)
    glUniformMatrix4fv(uniform_loc['M'], 1, GL_TRUE, c_matrix(ModelMatrix))
    glUniformMatrix4fv(uniform_loc['MVP'], 1, GL_TRUE, c_matrix(MVP))
    for i in range(len(obj.geom_nums)):
        glBindVertexArray(obj.vao_ids[i])
        # mtl parameter
        mtl = obj.mtl_buffer_list[i]
        glUniform3f(uniform_loc['material.ambient'], mtl.Ka[0], mtl.Ka[1], mtl.Ka[2])
        glUniform3f(uniform_loc['material.diffuse'], mtl.Kd[0], mtl.Kd[1], mtl.Kd[2])
        glUniform3f(uniform_loc['material.specular'], mtl.Ks[0], mtl.Ks[1], mtl.Ks[2])

        # texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, obj.texture_ids[i])
        glUniform1i(uniform_loc['myTextureSampler'], 0)

        # vertex
        glBindBuffer(GL_ARRAY_BUFFER, obj.vertex_buffer_ids[i])
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        # uv
        glBindBuffer(GL_ARRAY_BUFFER, obj.uv_buffer_ids[i])
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        # normal
        glBindBuffer(GL_ARRAY_BUFFER, obj.normal_buffer_ids[i])
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        # draw
        glDrawArrays(GL_TRIANGLES, 0, obj.geom_nums[i])

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glBindVertexArray(0)
    # flower3d
    obj = flowerObj
    ModelMatrix = scale(0.05)
    MVP = dots(ProjectionMatrix, ViewMatrix, ModelMatrix)
    glUniformMatrix4fv(uniform_loc['M'], 1, GL_TRUE, c_matrix(ModelMatrix))
    glUniformMatrix4fv(uniform_loc['MVP'], 1, GL_TRUE, c_matrix(MVP))
    for i in range(len(obj.geom_nums)):
        glBindVertexArray(obj.vao_ids[i])
        # mtl parameter
        mtl = obj.mtl_buffer_list[i]
        glUniform3f(uniform_loc['material.ambient'], mtl.Ka[0], mtl.Ka[1], mtl.Ka[2])
        glUniform3f(uniform_loc['material.diffuse'], mtl.Kd[0], mtl.Kd[1], mtl.Kd[2])
        glUniform3f(uniform_loc['material.specular'], mtl.Ks[0], mtl.Ks[1], mtl.Ks[2])

        # texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, obj.texture_ids[i])
        glUniform1i(uniform_loc['myTextureSampler'], 0)

        # vertex
        glBindBuffer(GL_ARRAY_BUFFER, obj.vertex_buffer_ids[i])
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        # uv
        glBindBuffer(GL_ARRAY_BUFFER, obj.uv_buffer_ids[i])
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        # normal
        glBindBuffer(GL_ARRAY_BUFFER, obj.normal_buffer_ids[i])
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        # draw
        glDrawArrays(GL_TRIANGLES, 0, obj.geom_nums[i])

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glBindVertexArray(0)

    # swap buffer
    glutSwapBuffers()


def update(val):
    if val == 1:
        glutPostRedisplay()
        # glutTimerFunc(int(1000 / FPS), update, 1)


def init_opengl():
    """set opengl parameter"""
    # depth test
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    # glEnable(GL_CULL_FACE)
    # glEnable(GL_LINE_SMOOTH)
    # glEnable(GL_BLEND)

    glClearColor(0.0, 0.0, 0.4, 0.0)


def init_texture():
    pass


def init_glut(argv):
    """glut initialization."""
    global window, g_camera
    glutInit(argv)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE)

    print(glutGet(GLUT_WINDOW_NUM_SAMPLES))
    window = glutCreateWindow(b'flower')

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(g_camera.keyboard)
    glutMouseFunc(g_camera.mouse)
    glutMouseWheelFunc(g_camera.mouseWheel)
    glutMotionFunc(g_camera.motion)
    glutTimerFunc(int(1000 / FPS), update, 1)


def init_shader():
    """load shader and set initial value"""
    global program_id, uniforms, uniform_loc
    program_id = BaseShaderProgram(
        'shaders/v_light.glsl', 'shaders/f_light.glsl').program_id
    # 'shaders/v_simple_texture.glsl', 'shaders/f_simple_texture.glsl').program_id
    # 'shaders/Transform.vs.glsl', 'shaders/f_green.glsl').program_id


    for uniform in uniforms:
        uniform_loc[uniform] = glGetUniformLocation(program_id, uniform)


def init_object():
    """load object data"""
    # read obj file
    global boxObj,flowerObj
    boxObj = Object(os.path.join('..', 'resources', 'box.obj'))
    boxObj.bind_buffer()
    flowerObj = Object(os.path.join('..', 'resources', 'flower3d.obj'))
    flowerObj.bind_buffer()


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
