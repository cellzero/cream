#version 330 core


in vec2 UV;
in vec3 vertexPos_worldspace;
in vec3 normal_cameraspace;
in vec3 eyeDir_cameraspace;
in vec3 lightDir_cameraspace;

out vec4 color;

struct Material
{
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};
struct Light {
    vec3 position_worldspace;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};
uniform sampler2D myTextureSampler;
uniform Material material;
uniform Light light;

void main() {

    vec3 MaterialDiffuseColor = texture( myTextureSampler, UV ).rgb;
//    vec3 MaterialDiffuseColor = vec3(0,0,0);

    // Ambient
    vec3 ambient = light.ambient * MaterialDiffuseColor;

    // Diffuse
    vec3 norm = normalize(normal_cameraspace);
    vec3 lightDir = normalize(lightDir_cameraspace);
    float diff = clamp(dot(norm, lightDir), 0, 1);
    vec3 diffuse = light.diffuse * diff * MaterialDiffuseColor;

    // Specular
    vec3 viewDir = normalize(eyeDir_cameraspace);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(clamp(dot(viewDir, reflectDir), 0, 1), material.shininess);
    vec3 specular = light.specular * (spec * MaterialDiffuseColor);

    vec3 result = ambient + diffuse + specular;
    color = vec4(result, 1.0f);
}
