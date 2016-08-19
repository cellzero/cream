from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileShader, compileProgram
from shader import BaseShaderProgram
import sys

WIDTH = 640
HEIGHT = 480
FPS = 50
ESC = b'\033'
SIZE_OF_FLOAT = 4

window = 0
vertex_array_id = 0
vertex_buffer_id = 0
triangle_program_id = 0

uniform_loc = {}
uniforms = []
g_vertex_buffer_data = [
    -1.0, -1.0, 0.0,
    1.0, -1.0, 0.0,
    0.0, 1.0, 0.0
]

def reshape(w, h):
    """TODO"""
    glViewport(0, 0, w, h)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(triangle_program_id)

    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glDisableVertexAttribArray(0)

    glutSwapBuffers()


def keyboard(key, x, y):
    print('key down', key, x, y)


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
    global triangle_program_id,uniforms,uniform_loc
    triangle_program_id =  BaseShaderProgram("shaders/v_none.glsl", "shaders/f_green.glsl").program_id

    for uniform in uniforms:
        uniform_loc[uniform] = glGetUniformLocation(triangle_program_id, uniform)


def init_object():
    """load object data"""
    global vertex_buffer_id, vertex_array_id
    # VAO
    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)

    vertex_buffer_id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
    vertex_buffer = (GLfloat * len(g_vertex_buffer_data))(*g_vertex_buffer_data)
    glBufferData(GL_ARRAY_BUFFER, len(g_vertex_buffer_data) * SIZE_OF_FLOAT,
                 vertex_buffer, GL_STATIC_DRAW)


def main(argv=None):
    global window

    if argv is None:
        argv = sys.argv
    init_glut(argv)
    init_opengl()
    init_shader()
    init_texture()
    init_object()
    glutMainLoop()


main()
