void main(void)
{
	vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution) / u_resolution.y;
	float d = 0.0;
	
	//	length gives scalar, so no abs is needed
	d = 0.05 / length(uv);

	gl_FragColor = vec4(vec3(d), 1.0);
}