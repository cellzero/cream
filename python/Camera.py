from OpenGL.GLUT import *
import numpy as np
from matrix_transform import clip, lookAt,normalize
from math import sin, cos,radians


KEY_W = b'w'
KEY_A = b'a'
KEY_S = b's'
KEY_D = b'd'
KEY_J = b'j'
KEY_K = b'k'
KEY_T = b't'


class Camera:
    def __init__(self,  position=np.array([0.0, 1.0, 3.0]),
                 lightPosition = np.array([2.0, 4.0, -2.0]),
                 front = np.array([0.0, 0.0, -1.0]),
                 right = np.array([1.0, 0.0, 0.0]),
                 up = np.array([0.0, 1.0, 0.0])
                 ):
        self.yaw = -90.0
        self.pitch = 0.0
        self.position = position
        self.zoom = 90.0
        self.moveSpeed = 1.0
        self.x0 = 0
        self.y0 = 0
        self.rotating = False
        self.translating = False  # translate camera y axis
        self.lightShifting = False # shift light position
        self.mouseSensitivity = 0.1
        self.front = front
        self.right = right
        self.up = up
        self.lightPosition = lightPosition
        self.scene = 'day'
        self.updateCameraVectors()


    def mouseWheel(self, button, dir, x, y):
        self.zoom -= dir
        self.zoom = clip(self.zoom, 1.0, 180.0)
        self.updateCameraVectors()
        glutPostRedisplay()


    def mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            self.rotating = (state == GLUT_DOWN)
        elif button == GLUT_RIGHT_BUTTON:
            self.translating = (state == GLUT_DOWN)
        elif button == GLUT_MIDDLE_BUTTON:
            self.lightShifting = (state == GLUT_DOWN)
        self.x0, self.y0 = x, y


    def keyboard(self, key, x, y):
        velocity = self.moveSpeed * 0.05

        if key == KEY_W:
            self.position += self.front * velocity
        elif key == KEY_S:
            self.position -= self.front * velocity
        elif key == KEY_A:
            self.position -= self.right * velocity
        elif key == KEY_D:
            self.position += self.right * velocity
        elif key == KEY_T:
            self.scene = 'night' if self.scene == 'day' else 'day'
        self.updateCameraVectors()
        glutPostRedisplay()

    def motion(self, x1, y1):
        velocity = self.moveSpeed * 0.05
        xoffset = (x1 - self.x0) * self.mouseSensitivity
        yoffset = (y1 - self.y0) * self.mouseSensitivity

        if self.rotating:
            self.yaw -= xoffset
            self.pitch += yoffset
            self.pitch = clip(self.pitch, -89, 89)
        elif self.translating:
            self.position += self.up * yoffset/8
        elif self.lightShifting:
            self.lightPosition += self.right* xoffset/16
            self.lightPosition -= self.up *yoffset/16

        self.x0, self.y0 = x1, y1
        self.updateCameraVectors()
        glutPostRedisplay()

    def getViewMatrix(self):
        return lookAt(self.position, self.position+self.front, self.up)
        # self.position =self.front *4
        # return lookAt(self.position, np.array([0,0,0]),np.array([0,1,0]))

    def updateCameraVectors(self):
        front_x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front_y = sin(radians(self.pitch))
        front_z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.front = normalize(np.array([front_x,front_y,front_z]))

        self.right = normalize(np.cross(self.front,np.array([0.0, 1.0, 0.0])))
        self.up = normalize(np.cross(self.right, self.front))


    def getLightPosition(self):
        return self.lightPosition


    def getScene(self):
        return self.scene

