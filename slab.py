import sys
import os
from mojoshader import Parser, ShaderType
from shaderlab import Blob
from ctypes import cast, c_char_p


with open(sys.argv[1], "rb") as fi:
	data = fi.read()
	p = Parser()
	b = Blob(data)

	for i, (t, s) in enumerate(b.shaders):
		m = p.parse(s)
		if m.error_count > 0:
			print(m.errors.contents.error)
		fname = "-".join(t)
		if m.shader_type == ShaderType.PIXEL:
			fname = "PS_" + fname
		elif m.shader_type == ShaderType.VERTEX:
			fname = "VS_" + fname

		out_file = os.path.join(sys.argv[2], fname + ".cg")
		with open(out_file, "w") as fo:
			fo.write(cast(m.output, c_char_p).value.decode("utf-8"))
