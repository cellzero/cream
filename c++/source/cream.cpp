#include "cream.h"
void cream::onResize(int w, int h)
{
}
void cream::onKey(int key, int action)
{
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
		glfwSetWindowShouldClose(window, GLFW_TRUE);
}
void cream::onMouseButton(int button, int action)
{
	if (GLFW_MOUSE_BUTTON_LEFT == button)
		this->mouse_lef_btn_pressed = (action == GLFW_PRESS);
}
void cream::onMouseMove(int x, int y)
{
	const float delta_unit_x = 360.0f / this->windowWidth*PI/180.0f;
	const float delta_unit_y = 360.0f / this->windowHeight*PI / 180.0f;
	if(mouse_lef_btn_pressed){
		horizontalAngle -= delta_unit_x * (x - mouse_pos_x);
		verticalAngle += delta_unit_y * (y - mouse_pos_y);
		verticalAngle = glm::clamp(verticalAngle, -PI/2, PI/2);
		//cout << verticalAngle << endl;
	}
	mouse_pos_x = x;
	mouse_pos_y = y;
}
void cream::onMouseWheel(int pos)
{
	radius -= pos;
}
void cream::error_callback(int error, const char * description)
{
	fprintf(stderr, "Error: %s\n", description);
}
void cream::compute_matrices()
{
}
cream::cream() {
	cream_pointer = this;
	windowWidth = 800;	windowHeight = 600;
	//set opengl version 
	gl_major_version = 3;	gl_minor_version = 3;
}

cream::~cream()
{
}



void cream::getMousePosition(int& x, int& y)
{
	double dx, dy;
	glfwGetCursorPos(window, &dx, &dy);

	x = static_cast<int>(floor(dx));
	y = static_cast<int>(floor(dy));
}
void cream::setWindowTitle(const char * title)
{
	glfwSetWindowTitle(window, title);
}

GLFWwindow* cream::initWindow() {
	GLFWwindow* window;

	// Initialise GLFW
	if (!glfwInit())
	{
		fprintf(stderr, "Failed to initialize GLFW\n");
		exit(EXIT_FAILURE);

	}

	glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, gl_major_version); // We want OpenGL 3.3
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, gl_minor_version);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); //We don't want the old OpenGL

																   // Open a window and create its OpenGL context
	window = glfwCreateWindow(this->windowWidth, this->windowHeight, "Simple example", NULL, NULL);
	if (!window)
	{
		glfwTerminate();
		exit(EXIT_FAILURE);
	}

	// Make the window's context current
	glfwMakeContextCurrent(window);

	// Set Callback hooks
	//glfwSetErrorCallback(error_callback);
	glfwSetWindowSizeCallback(window, cream::glfw_onResize);
    glfwSetKeyCallback(window, cream::glfw_onKey);
    glfwSetMouseButtonCallback(window, cream::glfw_onMouseButton);
    glfwSetCursorPosCallback(window, cream::glfw_onMouseMove);
    glfwSetScrollCallback(window, cream::glfw_onMouseWheel);

	// Initialize GLEW
	glewExperimental = true; // Needed in core profile
	GLenum err = glewInit();
	if (GLEW_OK != err)
	{
		/* Problem: glewInit failed, something is seriously wrong. */
		fprintf(stderr, "Error: %s\n", glewGetErrorString(err));
		glfwTerminate();
	}

	return window;
}


void cream::run() {
	this->window = initWindow();

	startup();

	while (!glfwWindowShouldClose(window)) {
		render(glfwGetTime());

		/* Swap front and back buffers */
		glfwSwapBuffers(window);
		/* Poll for and process events */
		glfwPollEvents();
	}

	shutdown();
	glfwDestroyWindow(window);
	glfwTerminate();
	exit(EXIT_SUCCESS);
}

void cream::startup()
{
	// Dark blue background
	glClearColor(0.0f, 0.0f, 0.4f, 0.0f);
	// Enable depth test
	glEnable(GL_DEPTH_TEST);
	// Accept fragment if it closer to the camera than the former one
	glDepthFunc(GL_LESS);
	// Cull triangles which normal is not towards the camera
	glEnable(GL_CULL_FACE);

	//glEnable(GL_BLEND);
	//glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	// Create and compile our GLSL program from the shaders
	this->programID = LoadShaders("../source/shader/StandardShading.vertexshader", "../source/shader/StandardShading.fragmentshader");
	// Load the texture using any two methods
	this->TextureID = loadDDS("../source/texture/uvmap.DDS");
	// Read our .obj file
	loadOBJ("../source/obj/suzanne.obj", vertices, uvs, normals);

	glGenVertexArrays(1, &(this->VertexArrayID));
	glBindVertexArray(this->VertexArrayID);

	// Get uniforms' ID of variables in shader
	MatrixID = glGetUniformLocation(programID, "MVP");
	ViewMatrixID = glGetUniformLocation(programID, "V");
	ModelMatrixID = glGetUniformLocation(programID, "M");
	myTextureSamplerID = glGetUniformLocation(programID, "myTextureSampler");
	LightID = glGetUniformLocation(programID, "LightPosition_worldspace");

	// This will identify our vertex buffer
	glGenBuffers(1, &vertexbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
	glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(glm::vec3), &vertices[0], GL_STATIC_DRAW);

	glGenBuffers(1, &normalbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, normalbuffer);
	glBufferData(GL_ARRAY_BUFFER, normals.size() * sizeof(glm::vec3), &normals[0], GL_STATIC_DRAW);

	/*GLuint colorbuffer;
	glGenBuffers(1, &colorbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, colorbuffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(g_color_buffer_data), g_color_buffer_data, GL_STATIC_DRAW);*/

	glGenBuffers(1, &uvbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, uvbuffer);
	glBufferData(GL_ARRAY_BUFFER, uvs.size() * sizeof(glm::vec2), &uvs[0], GL_STATIC_DRAW);

	//set initial mouse position
	getMousePosition(mouse_pos_x, mouse_pos_y);
	horizontalAngle = 0;
	verticalAngle = 0;
	radius = 4;

	fps = 0;
	lastTime = glfwGetTime();
	//init text2d
	initText2D("../source/texture/Holstein.DDS");
}

void cream::render(double currentTime)
{
	//calculate fps
	fps++;
	if (currentTime - lastTime >= 1.0) { // If last prinf() was more than 1sec ago
										 // printf and reset
		char window_title[100];
		sprintf(window_title,"fps=%d", fps);
		setWindowTitle(window_title);
		fps = 0;
		lastTime = currentTime;
	}
	// Clear the screen
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// Use our shader
	glUseProgram(programID);

	// Send our transformation to the currently bound shader, 
	// in the "MVP" uniform
	
	Projection = glm::perspective(45.0f, 4.0f / 3.0f, 0.1f, 100.0f);
	glm::vec3 direction(
		cos(verticalAngle) * sin(horizontalAngle),
		sin(verticalAngle),
		cos(verticalAngle) * cos(horizontalAngle)
	);
	glm::vec3 position = glm::mat3(radius) * direction;
	View = glm::lookAt(
		position,
		glm::vec3(0, 0, 0), // and looks at the origin
		glm::vec3(0, 1, 0)  // Head is up (set to 0,-1,0 to look upside-down)
	);
	Model = glm::mat4(1.0f);
	MVP = Projection * View * Model; // Remember, matrix multiplication is the other way around

	glUniformMatrix4fv(MatrixID, 1, GL_FALSE, &MVP[0][0]);
	glUniformMatrix4fv(ModelMatrixID, 1, GL_FALSE, &Model[0][0]);
	glUniformMatrix4fv(ViewMatrixID, 1, GL_FALSE, &View[0][0]);

	//set light position
	glm::vec3 lightPos = glm::vec3(4, 4, 4);
	glUniform3f(LightID, lightPos.x, lightPos.y, lightPos.z);
	//glUniform3f(LightID, position.x,position.y,position.z);

	// Bind our texture in Texture Unit 0
	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, TextureID);
	// Set our "myTextureSampler" sampler to user Texture Unit 0
	glUniform1i(myTextureSamplerID, 0);

	// 1rst attribute buffer : vertices
	glEnableVertexAttribArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
	glVertexAttribPointer(
		0,                  // attribute. No particular reason for 0, but must match the layout in the shader.
		3,                  // size
		GL_FLOAT,           // type
		GL_FALSE,           // normalized?
		0,                  // stride
		(void*)0            // array buffer offset
	);

	// 2nd attribute buffer : colors
	glEnableVertexAttribArray(1);
	glBindBuffer(GL_ARRAY_BUFFER, uvbuffer);
	glVertexAttribPointer(
		1,                                // attribute. No particular reason for 1, but must match the layout in the shader.
		2,                                // size : U+V => 2
		GL_FLOAT,                         // type
		GL_FALSE,                         // normalized?
		0,                                // stride
		(void*)0                          // array buffer offset
	);
	glEnableVertexAttribArray(2);
	glBindBuffer(GL_ARRAY_BUFFER, normalbuffer);
	glVertexAttribPointer(
		2,                                // attribute
		3,                                // size
		GL_FLOAT,                         // type
		GL_FALSE,                         // normalized?
		0,                                // stride
		(void*)0                          // array buffer offset
	);

	// Draw the triangle !
	glDrawArrays(GL_TRIANGLES, 0, vertices.size());

	glDisableVertexAttribArray(0);
	glDisableVertexAttribArray(1);
	glDisableVertexAttribArray(2);

	char text[256];
	sprintf(text, "%.2f sec", glfwGetTime());
	printText2D(text, 10, 500, 40);
}

void cream::shutdown()
{
	// Cleanup VBO
	glDeleteBuffers(1, &vertexbuffer);
	//glDeleteBuffers(1, &colorbuffer);
	glDeleteTextures(1, &TextureID);

	glDeleteVertexArrays(1, &VertexArrayID);
	glDeleteProgram(programID);
}