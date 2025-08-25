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
void main(void)
{
	vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution) / u_resolution.y;
	float d = 0.0;
	
	//	length gives scalar, so no abs is needed
	d = 0.05 / length(uv);

	gl_FragColor = vec4(vec3(d), 1.0);
}