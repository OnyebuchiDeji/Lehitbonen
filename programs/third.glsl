void main(void)
{
	vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution) / u_resolution.y;

	float d = 0.0;
	d = 0.05 / length(uv);
/**
	when d is less than 0.1, for the pixels further
 from the center of the screen, it's capped to 0.0 (black), and for those closer to the screen such that the d value produced is >= 0.8, they're capped to 1.0
*/
	//d = smoothstep(0.1, 0.8, d);

	//	the inverse
	d = smoothstep(0.8, 0.1, d);

	gl_FragColor = vec4(vec3(d), 1.0);
}