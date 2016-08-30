#version 330 core

uniform vec3 lightColor;
out vec3 color;
void main() {
//    color = vec4(1,1,1,1.0f);
    color = lightColor;
}
