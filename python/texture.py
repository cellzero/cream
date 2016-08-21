from OpenGL.GL import *
from PIL import Image

texture_cache = {}


def bind_texture(image, format):
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes('raw', format, 0, -1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)
    # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return texture_id


def load_texture(file_name, format='RGBA'):
    try:
        cache_key = '{0}|{1}'.format(file_name, format)
        return texture_cache[cache_key]
    except KeyError:
        image = Image.open(file_name).convert(format)
        texture_id = bind_texture(image, format)
        texture_cache[cache_key] = texture_id
        return texture_id
