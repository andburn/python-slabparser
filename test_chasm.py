from unityasm import parse_line

def test_mad_1():
    assert parse_line("mad r0, r0, r1.x, c5") == "r0 = vec4(r0 * r1.x + c5);"

def test_mad_2():
    assert parse_line("mad oT0.xy, v1, c7, c7.zwzw") == "oT0.xy = vec2(v1 * c7 + c7.zwzw);"
