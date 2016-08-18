#pragma once
// Include standard headers
#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include <cmath>
// Include GLEW. Always include it before gl.h and glfw.h, since it's a bit magic.
#include <GL/glew.h>
// Include GLFW
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

#include "common/shader.hpp"
#include "common/texture.hpp"
#include "common/objloader.hpp"
#include "common\text2D.hpp"

using namespace glm;
using namespace std;
#define PI (3.1415925f)

class cream;
static cream * cream_pointer;

class cream
{
private:
	
	GLFWwindow* window;
	int windowWidth,windowHeight;
	int gl_major_version, gl_minor_version;
	glm::mat4 View, Model, Projection, MVP;
	glm::vec3 camera_pos;

	/* IDs */
	GLuint programID; //shader program
	GLuint VertexArrayID;
	GLuint TextureID;

	/* render data */
	std::vector<glm::vec3> vertices;
	std::vector<glm::vec2> uvs;
	std::vector<glm::vec3> normals; // Won't be used at the moment.

	/* Uniform variables */
	GLuint myTextureSamplerID, MatrixID, ViewMatrixID, ModelMatrixID;
	GLuint LightID;
	/* buffer */
	GLuint vertexbuffer, uvbuffer, colorbuffer, normalbuffer;

	GLfloat verticalAngle, horizontalAngle;  //in radian
	GLfloat radius;

	int mouse_pos_x, mouse_pos_y;

	int fps;
	double lastTime;

	/* mouse and keyboard control */
	bool mouse_lef_btn_pressed = false;

	static void glfw_onResize(GLFWwindow* window, int w, int h)
	{
		cream_pointer->onResize(w, h);
	}

	static void glfw_onKey(GLFWwindow* window, int key, int scancode, int action, int mods)
	{
		cream_pointer->onKey(key, action);
	}

	static void glfw_onMouseButton(GLFWwindow* window, int button, int action, int mods)
	{
		cream_pointer->onMouseButton(button, action);
	}

	static void glfw_onMouseMove(GLFWwindow* window, double x, double y)
	{
		cream_pointer->onMouseMove(static_cast<int>(x), static_cast<int>(y));
	}

	static void glfw_onMouseWheel(GLFWwindow* window, double xoffset, double yoffset)
	{
		cream_pointer->onMouseWheel(static_cast<int>(yoffset));
	}
	static void glfw_error_callback(int error, const char* description) {
		cream_pointer->error_callback(error, description);
	}
public:
	
	cream();
	~cream();
	GLFWwindow* initWindow();
	void run();
	void startup();
	void render(double currentTime);
	void shutdown();
	void getMousePosition(int& x, int& y);
	void setWindowTitle(const char * title);
	/* hooks function */
	void onResize(int w, int h);
	void onKey(int key, int action);
	void onMouseButton(int button, int action);
	void onMouseMove(int x, int y);
	void onMouseWheel(int pos);
	void error_callback(int error, const char* description);
	void compute_matrices();
};

