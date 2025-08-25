---VERTEX SHADER-------------------------------------------------------
#version 330 core

#ifdef GL_ES
    precision highp float;
#endif

attribute vec2 in_pos;

void main (void) {
    gl_Position = vec4(in_pos, 0.0, 1.0);
}


---FRAGMENT SHADER-----------------------------------------------------
#version 330 core

#ifdef GL_ES
    precision highp float;
#endif

uniform vec2 u_resolution;
uniform float u_time;

void main_v1()
{
    vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution.xy) / u_resolution.x;
    vec3 color = vec3(0.0);

    uv = step(0.0, uv);
    color = vec3(uv, 0.0);

    gl_FragColor = vec4(color, 1.0);
}
void main_v2()
{
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    gl_FragColor = vec4(uv, 1.0 - uv.x, 1.0);
}
void main_v3()
{
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    vec3 col = vec3(uv, 0.5 + 0.5 * sin(u_time));
    gl_FragColor = vec4(col, 1.0);
}

void main (void){
    //main_v1();
    //main_v2();
    main_v3();
}