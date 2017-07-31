import sys
import os
from mojoshader import Parser, ShaderType, Usage, UniformType, SymbolRegisterSet
from shaderlab import Blob
from ctypes import cast, c_char_p
from operator import attrgetter


class UniformSymbol:
	def __init__(self, name, type, index):
		self.name = name.decode("ascii")
		self.type = type
		self.index = index

	def __str__(self):
		return "%s %d [%d]" % (self.name, self.type, self.index)

	def str_assign(self):
		return "uniform vec4 %s;" % (self.name)

	def str_define(self, is_pixel_shader=False):
		prefix = "ps" if is_pixel_shader else "vs"
		return "#define %s_c%d %s" % (prefix, self.index, self.name)


with open(sys.argv[1], "rb") as fi:
	data = fi.read()
	p = Parser()
	b = Blob(data)

	for i, (t, s) in enumerate(b.shaders):
		try:
			m = p.parse(s)
		except Exception as e:
			print("Parse failed on %d: %s" % (i, e))
			continue

		if m.error_count > 0:
			print(m.errors.contents.error)
		fname = "-".join(t)
		if m.shader_type == ShaderType.PIXEL:
			fname = "PS_" + fname
			is_pixel = True
		elif m.shader_type == ShaderType.VERTEX:
			fname = "VS_" + fname
			is_pixel = False

		out_file = os.path.join(sys.argv[2], fname + ".cg")

		defs = []
		defs.append("//-- %d Symbols" % (m.symbol_count))
		symbols = []
		tex_symbols = []
		for j in range(m.symbol_count):
			sym = UniformSymbol(m.symbols[j].name, m.symbols[j].register_set, m.symbols[j].register_index)
			if m.symbols[j].register_set == 3:
				tex_symbols.append(sym)
			else:
				symbols.append(sym)
		symbols.sort(key=attrgetter("index"))
		tex_symbols.sort(key=attrgetter("index"))
		defs = defs + [s.str_assign() for s in symbols] + [s.str_define(is_pixel) for s in symbols] + ["//-- Samplers"] + [str(s) for s in tex_symbols]

		defs.append("//-- %d Attributes" % (m.attribute_count))
		for j in range(m.attribute_count):
			defs.append("// %s %s %d" % (m.attributes[j].name, Usage(m.attributes[j].usage), m.attributes[j].index))

		defs.append("//-- %d Uniforms" % (m.uniform_count))
		for j in range(m.uniform_count):
			defs.append("// %s %s %d %d %d" % (m.uniforms[j].name, UniformType(m.uniforms[j].type), m.uniforms[j].array_count, m.uniforms[j].index, m.uniforms[j].constant))

		with open(out_file, "w") as fo:
			fo.write("\r".join(defs))
			fo.write("\r\r")
			fo.write(str(m).replace("\n", ""))
