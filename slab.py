import sys
import os
import mojoshader
import shaderlab
import ctypes


with open(sys.argv[1], "rb") as f:
	data = f.read()

p = mojoshader.Parser()
b = shaderlab.Blob(data)
for i, (t, s) in enumerate(b.shaders):
	m = p.parse(s)
	if m.error_count > 0:
		print(m.errors.contents.error)
	print(m.profile, m.error_count, m.output_len)
	print(t)
	print(ctypes.cast(m.output, ctypes.c_char_p).value)
