/*
 * helloglut.cpp
 *
 *  Created on: 2016年4月22日
 *      Author: cellzero
 */

#include <GL/gl.h>
#include <GL/freeglut.h>

static void RenderScene(void) {
	glClear(GL_COLOR_BUFFER_BIT);
	glFlush();
}

static void SetupRC(void) {
	glClearColor(0.0f, 0.0f, 1.0f, 1.0f);
}

int main(int argc, char *argv[]) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA);
	glutCreateWindow("Hello Free GLUT");
	glutDisplayFunc(RenderScene);

	SetupRC();
	glutMainLoop();

	glutExit();
	return 0;
}
