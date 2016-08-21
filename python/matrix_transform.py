from ctypes import sizeof, c_float, c_void_p, c_uint, string_at
from numpy import dot, cross
import numpy
from math import (cos as _cos, sin as _sin, atan2 as _atan2, asin as _asin,
sqrt as _sqrt)
import vector as _v



def normalize(vector):
    return vector / numpy.linalg.norm(vector)


def translate(tx=0.0, ty=0.0, tz=0.0):
    result = numpy.array(
        [[1., 0., 0., tx],
         [0., 1., 0., ty],
         [0., 0., 1., tz],
         [0., 0., 0., 1.]]
    )
    return result


def scale(s):
    result = numpy.array(
        [[s, 0.0, 0.0, 0.0],
         [0.0, s, 0.0, 0.0],
         [0.0, 0.0, s, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
    )
    return result


def lookAt(eye, center, up):
    f = normalize(center - eye)
    s = normalize(cross(f, up))
    u = normalize(cross(s, f))

    Result = numpy.array([[s[0], u[0], -f[0], 0],
                          [s[1], u[1], -f[1], 0],
                          [s[2], u[2], -f[2], 0],
                          [-dot(s,eye),-dot(u,eye),dot(f,eye),1]], dtype=numpy.float32)
    return Result.T


def perspective(fovy, aspect, zNear, zFar):
    tanHalfFovy = numpy.tan(fovy / 2)

    Result = numpy.zeros((4, 4), dtype=numpy.float32)

    Result[0][0] = 1 / (aspect * tanHalfFovy)
    Result[1][1] = 1 / tanHalfFovy
    Result[2][2] = - (zFar + zNear) / (zFar - zNear)
    Result[2][3] = - 1
    Result[3][2] = - (2 * zFar * zNear) / (zFar - zNear)
    return Result.T


def c_matrix(matrix):
    matrix_array = [float(a) for line in matrix for a in line]
    return (c_float * 16)(*matrix_array)

# ViewMatrix = lookAt(
#         numpy.array([4,4,3]),
#         numpy.array([0,0,0]),
#         numpy.array([0,1,0])
# )

def scale(sx=1., sy=1., sz=1.):
    return numpy.array(
            [[sx, 0., 0., 0.],
	        [0., sy, 0., 0.],
	        [0., 0., sz, 0.],
	        [0., 0., 0., 1.]])

def euler_angles(Q):
    w, (x, y, z) = Q
    phi   = _atan2(2.*(w*x+y*z), 1.-2.*(x*x+y*y))
    theta = _asin(2*(w*y-x*z))
    psi   = _atan2(2.*(w*z+x*y), 1.-2.*(y*y+z*z))
    return phi, theta, psi


def translate(tx=0., ty=0., tz=0.):
    return numpy.array(
           [[1., 0., 0., tx],
	        [0., 1., 0., ty],
	        [0., 0., 1., tz],
	        [0., 0., 0., 1.]])


def arcball(x, y):
    h2 = x*x+y*y
    if h2 > 1.:
        h = _sqrt(h2)
        v = x/h, y/h, 0.
    else:
        v = x, y, _sqrt(1.-h2)
    return 0., v

def quaternion(theta=0, u=(1., 0., 0.)):
    w = _cos(theta/2.)
    x, y, z = (ui*_sin(theta/2.) for ui in u)
    return w, (x, y, z)

def mul(P, Q):
    w1, v1 = P
    w2, v2 = Q
    return (w1*w2 - _v.dot(v1, v2),_v.sum(_v.mul(w1, v2), _v.mul(w2, v1), _v.cross(v1, v2)))

def product(P=quaternion(), *Qs):
    for Q in Qs:
        P = mul(P, Q)
    return P
def matrix(Q):
    w, (x, y, z) = Q
    return numpy.array(
            [[1.-2.*(y*y+z*z), 2.*(x*y+w*z),    2.*(x*z-w*y),   0.],
            [2.*(x*y-w*z),    1.-2.*(x*x+z*z), 2.*(y*z+w*x),    0.],
            [2.*(x*z+w*y),    2.*(y*z-w*x),    1.-2.*(x*x+y*y), 0.],
            [0.,              0.,              0.,              1.]])

def dots(P, *Qs):
    Result = P
    for Q in Qs:
        Result = numpy.dot(Result, Q)
    return Result

def rotate(m,angle,v):

    c = _cos(angle)
    s = _sin(angle)

    axis = normalize(v)
    temp =(1. - c) * axis

    Rotate = numpy.zeros((4, 4), 'f')
    Rotate[0][0] = c + temp[0] * axis[0]
    Rotate[0][1] = 0 + temp[0] * axis[1] + s * axis[2]
    Rotate[0][2] = 0 + temp[0] * axis[2] - s * axis[1]

    Rotate[1][0] = 0 + temp[1] * axis[0] - s * axis[2]
    Rotate[1][1] = c + temp[1] * axis[1]
    Rotate[1][2] = 0 + temp[1] * axis[2] + s * axis[0]

    Rotate[2][0] = 0 + temp[2] * axis[0] + s * axis[1]
    Rotate[2][1] = 0 + temp[2] * axis[1] - s * axis[0]
    Rotate[2][2] = c + temp[2] * axis[2]

    Result = numpy.zeros((4, 4), 'f')
    Result[0] = m[0] * Rotate[0][0] + m[1] * Rotate[0][1] + m[2] * Rotate[0][2]
    Result[1] = m[0] * Rotate[1][0] + m[1] * Rotate[1][1] + m[2] * Rotate[1][2]
    Result[2] = m[0] * Rotate[2][0] + m[1] * Rotate[2][1] + m[2] * Rotate[2][2]
    Result[3] = m[3]
    return Result.T
