from ctypes import sizeof, c_float, c_void_p, c_uint, string_at
from numpy import dot,cross
import numpy

def normalize(vector):
    return vector/numpy.linalg.norm(vector)

def lookAt(eye,center,up):
    f = normalize(center - eye)
    s = normalize(cross(f, up))
    u = normalize(cross(s, f))

    result = numpy.array([[s[0], u[0], -f[0], 0],
                          [s[1], u[1], -f[1], 0],
                          [s[2], u[2], -f[2], 0],
                          [-dot(s,eye),-dot(u,eye),dot(f,eye),1]], dtype=numpy.float32)
    return result


def perspective(fovy, aspect, zNear, zFar):
    tanHalfFovy = numpy.tan(fovy / 2)

    Result = numpy.zeros((4, 4), dtype=numpy.float32)

    Result[0][0] = 1 / (aspect * tanHalfFovy)
    Result[1][1] = 1 / tanHalfFovy
    Result[2][2] = - (zFar + zNear) / (zFar - zNear)
    Result[2][3] = - 1
    Result[3][2] = - (2 * zFar * zNear) / (zFar - zNear)
    return Result

def c_matrix(matrix):
    matrix_array =  [float(a) for line in matrix for a in line]
    return (c_float*16)(*matrix_array)

# ViewMatrix = lookAt(
#         numpy.array([4,4,3]),
#         numpy.array([0,0,0]),
#         numpy.array([0,1,0])
# )
