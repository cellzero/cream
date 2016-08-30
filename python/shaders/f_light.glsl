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
struct Light
{
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform Light light;
uniform vec3 lightPos_worldspace;
uniform sampler2D myTextureSampler;
uniform Material material;
uniform vec3 lightColor;

void main() {

//    vec3 lightColor = vec3(20.0/255, 60.0/255, 180.0/255);
    float LightPower = 20;
    vec3 MaterialDiffuseColor = texture( myTextureSampler, UV ).rgb;

    float distance = length(lightPos_worldspace - vertexPos_worldspace);

    // Ambient
    vec3 ambient = material.ambient * MaterialDiffuseColor;

    // Diffuse
    vec3 norm = normalize(normal_cameraspace);
    vec3 lightDir = normalize(lightDir_cameraspace);
    float diff = clamp(dot(norm, lightDir), 0, 1);
    vec3 diffuse = lightColor *material.diffuse * diff * LightPower* MaterialDiffuseColor/pow(distance,2);

    // Specular
    vec3 viewDir = normalize(eyeDir_cameraspace);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(clamp(dot(viewDir, reflectDir), 0, 1), material.shininess);
    vec3 specular = lightColor *material.specular * (LightPower *spec * MaterialDiffuseColor)/pow(distance,2);

    vec3 result = light.ambient * ambient +
                  light.diffuse * diffuse +
                  light.specular*specular;
    color = vec4(result,1.0f);
}
