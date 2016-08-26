#version 330 core
layout (location = 0) in vec3 vertexPos_modelspace;
layout(location = 1) in vec3 vertexUV;
layout (location = 2) in vec3 normal_modelspace;


uniform sampler2D myTextureSampler;
uniform mat4 MVP;
uniform mat4 V;
uniform mat4 M;
//uniform mat3 NormalMatrix;
uniform vec3 lightPos_worldspace;
out vec2 UV;

out vec3 vertexPos_worldspace;
out vec3 normal_cameraspace;
out vec3 eyeDir_cameraspace;
out vec3 lightDir_cameraspace;


void main() {

    gl_Position = MVP * vec4(vertexPos_modelspace, 1.0f);

    normal_cameraspace = (V * M * vec4(normal_modelspace,0)).xyz;
//    normal_cameraspace = (V * M * vec4(NormalMatrix * normal_modelspace,0)).xyz;

    vertexPos_worldspace = (M * vec4(vertexPos_modelspace,1)).xyz;

    vec3 vertexPos_cameraspace = (V * M * vec4(vertexPos_modelspace,1)).xyz;
    eyeDir_cameraspace = vec3(0,0,0) - vertexPos_cameraspace;

    vec3 LightPosition_cameraspace = (V * vec4(lightPos_worldspace,1)).xyz;
	lightDir_cameraspace = LightPosition_cameraspace + eyeDir_cameraspace;

	UV = vertexUV.xy;
}
