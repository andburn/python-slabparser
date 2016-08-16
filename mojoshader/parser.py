import os
import ctypes
import ctypes.util
import mojoshader


class LibraryNotFoundException(OSError):
	pass


def load_lib(*names):
	for name in names:
		try:
			libname = ctypes.util.find_library(name)
			if libname:
				return ctypes.CDLL(libname)
			else:
				dll_path = os.path.join(os.getcwd(), "lib%s.dll" % (name))
				return ctypes.CDLL(dll_path)
	raise LibraryNotFoundException("Could not load the library %r" % (names[0]))


class Parser:
	def __init__(self):
		self.lib = load_lib("mojoshader")

	def parse(self, data):
		self.lib.MOJOSHADER_parse.argtypes = [
			ctypes.c_char_p,
			ctypes.c_char_p,
			ctypes.POINTER(ctypes.c_char),
			ctypes.c_int,
			ctypes.POINTER(mojoshader.Swizzle),
			ctypes.c_int,
			ctypes.POINTER(mojoshader.SamplerMap),
			ctypes.c_int,
			ctypes.c_void_p, # MOJOSHADER_malloc
			ctypes.c_void_p, # MOJOSHADER_free
			ctypes.c_void_p
		]
		self.lib.MOJOSHADER_parse.restype = ctypes.POINTER(mojoshader.ParseData)

		return self.lib.MOJOSHADER_parse(
			"glsl",
			"main",
			data,
			len(data),
			None, 0,
			None, 0,
			None, None, None).contents
