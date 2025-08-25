

void main(void)
{
	vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution) / u_resolution.y;
	uv *= sin(u_time) + 0.15;
	gl_FragColor = vec4(uv, 0.0, 1.0);
}