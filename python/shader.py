from OpenGL.GL import *
from OpenGL.GL.shaders import *
import os.path


class BaseShaderProgram:
    """
    Helper class for using GLSL shader programs
    """

    def __init__(self, vertex, fragment):
        """
        :param vertex: str
            String containing shader file path or source code for the vertex shader
        :param fragment:
            String containing shader file path or source code for the fragment shader
        """
        self.program_id = glCreateProgram()
        v_id = self.add_shader(vertex, GL_VERTEX_SHADER)
        frag_id = self.add_shader(fragment, GL_FRAGMENT_SHADER)

        glAttachShader(self.program_id, v_id)
        glAttachShader(self.program_id, frag_id)
        glLinkProgram(self.program_id)

        if glGetProgramiv(self.program_id, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(self.program_id)
            glDeleteProgram(self.program_id)
            glDeleteShader(v_id)
            glDeleteShader(frag_id)
            raise RuntimeError('Error linking program: {0}'.format(info))
        glDeleteShader(v_id)
        glDeleteShader(frag_id)

    def add_shader(self, shader_str, shader_type):
        """
        Helper function for loading and compiling a GLSL shader
        :param shader_str:
        :param shader_type: valid OpenGL shader type
            Type of shader to compile
        :return: int
            Identifier for shader if compilation is successful
        """
        source = shader_str
        if os.path.exists(shader_str):
            source = self.load_shader(shader_str)
        return self.compile_shader(source, shader_type)

    @staticmethod
    def load_shader(shader_path):
        """
        Loading shader from file
        :param shader_path: str
            String containing shader file path for the vertex shader
        :return: str
            String containing shader source code
        """
        fin = open(shader_path, 'r')
        source = fin.read()
        fin.close()
        return source

    @staticmethod
    def compile_shader(source, shader_type):
        """
        Compiling shader
        :param source: str
            String containing shader source code
        :param shader_type: valid OpenGL shader type
            Type of shader to compile
        :return: int
            Identifier for shader if compilation is successful
        """
        try:
            shader_id = glCreateShader(shader_type)
            glShaderSource(shader_id, source)
            glCompileShader(shader_id)
            if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
                info = glGetShaderInfoLog(shader_id)
                raise RuntimeError('Shader compilation failed: {0}'.format(info))
            return shader_id
        except:
            glDeleteShader(shader_id)
            raise

    def uniform_location(self, uni_name):
        return glGetUniformLocation(self.program_id, uni_name)

    def attribute_location(self, attr_name):
        return glGetAttribLocation(self.program_id, attr_name)
