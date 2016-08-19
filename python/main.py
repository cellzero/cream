from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileShader, compileProgram
import sys

WIDTH = 640
HEIGHT = 480
FPS = 50
ESC = b'\033'
SIZE_OF_FLOAT = 4

window = 0
vertex_array_id = 0
vertex_buffer = 0
triangle_program = 0
g_vertex_buffer_data = [
    -1.0, -1.0, 0.0,
    1.0, -1.0, 0.0,
    0.0, 1.0, 0.0
]
g_vertex_shader_str = """
#version 330 core
layout(location = 0) in vec3 vertexPosition_modelSpace;
void main(){
gl_Position.xyz = vertexPosition_modelSpace;
gl_Position.w = 1.0;
}
"""
g_fragment_shader_str = """
#version 330 core
out vec3 color;
void main()
{
color = vec3(1,0,0);
}
"""


def reshape(w, h):
    """TODO"""
    glViewport(0, 0, w, h)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(triangle_program)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
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


def load_shader():
    """TODO """


def init_opengl():
    """set opengl parameter"""
    # depth test
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    global vertex_buffer, vertex_array_id
    glClearColor(0.0, 0.0, 0.4, 0.0)
    # VAO
    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    array_type = (GLfloat * len(g_vertex_buffer_data))
    glBufferData(
        GL_ARRAY_BUFFER, len(g_vertex_buffer_data) * SIZE_OF_FLOAT,
        array_type(*g_vertex_buffer_data), GL_STATIC_DRAW)




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

def motion(x1, y1):
    print(x1," ",y1)

def init_shader():
    """load shader and set initial value"""
    global triangle_program
    # Shader
    triangle_program = compileProgram(
        compileShader(g_vertex_shader_str, GL_VERTEX_SHADER),
        compileShader(g_fragment_shader_str, GL_FRAGMENT_SHADER)
    pass

def init_object():
    """load object data"""
    pass

def main(argv=None):
    global window

    if argv is None:
        argv = sys.argv
    init_glut(argv)
    init_opengl()
    init_shader()
    init_object()
    glutMainLoop()

main()
