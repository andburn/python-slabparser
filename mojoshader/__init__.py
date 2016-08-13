import os
import ctypes
from enum import IntEnum


class LibraryNotFoundException(OSError):
	pass


class MojoShaderError(ctypes.Structure):
	_fields_ = [
		("error", ctypes.c_char_p),
		("filename", ctypes.c_char_p),
		("error_position", ctypes.c_int)
	]


class MojoShaderSwizzle(ctypes.Structure):
	_fields_ = [
		("usage", ctypes.c_int), # enum MOJOSHADER_usage
		("index", ctypes.c_int),
		("swizzles", ctypes.c_char * 4)
	]


class MojoShaderUniform(ctypes.Structure):
	_fields_ = [
		("type", ctypes.c_int), # enum MOJOSHADER_uniformType
		("index", ctypes.c_int),
		("array_count", ctypes.c_int),
		("constant", ctypes.c_int),
		("name", ctypes.c_char_p)
	]


class MojoShaderConstantUniform(ctypes.Union):
	_fields_ = [
		("f", ctypes.c_float * 4),
		("i", ctypes.c_int * 4),
		("b", ctypes.c_int),
	]


class MojoShaderConstant(ctypes.Structure):
	_fields_ = [
		("type", ctypes.c_int), # enum MOJOSHADER_uniformType
		("index", ctypes.c_int),
		("value", MojoShaderConstantUniform)
	]


class MojoShaderSampler(ctypes.Structure):
	_fields_ = [
		("type", ctypes.c_int), # enum MOJOSHADER_samplerType
		("index", ctypes.c_int),
		("name", ctypes.c_char_p),
		("texbem", ctypes.c_int)
	]


class MojoShaderSamplerMap(ctypes.Structure):
	_fields_ = [
		("index", ctypes.c_int),
		("type", ctypes.c_int), # enum MOJOSHADER_samplerType
	]


class MojoShaderAttribute(ctypes.Structure):
	_fields_ = [
		("usage", ctypes.c_int), # enum MOJOSHADER_usage
		("index", ctypes.c_int),
		("name", ctypes.c_char_p)
	]


class MojoShaderSymbolTypeInfo(ctypes.Structure):
	_fields_ = [
		("parameter_class", ctypes.c_int), # enum MOJOSHADER_symbolClass
		("parameter_type", ctypes.c_int), # enum MOJOSHADER_symbolType
		("rows", ctypes.c_uint),
		("columns", ctypes.c_uint),
		("elements", ctypes.c_uint),
		("member_count", ctypes.c_uint)
	]


class MojoShaderSymbolStructMember(ctypes.Structure):
	_fields_ = [
		("name", ctypes.c_char_p),
		("info", ctypes.POINTER(MojoShaderSymbolTypeInfo))
	]


class MojoShaderSymbol(ctypes.Structure):
	_fields_ = [
		("name", ctypes.c_char_p),
		("register_set", ctypes.c_int), # enum MOJOSHADER_symbolRegisterSet
		("register_index", ctypes.c_uint),
		("register_count", ctypes.c_uint),
		("info", ctypes.POINTER(MojoShaderSymbolTypeInfo)),
	]


class MojoShaderPreShaderOperand(ctypes.Structure):
	_fields_ = [
		("type", ctypes.c_int), # enum MOJOSHADER_preshaderOperandType
		("index", ctypes.c_uint),
		("array_register_count", ctypes.c_uint),
		("array_registers", ctypes.POINTER(ctypes.c_uint))
	]


class MojoShaderPreShaderInstruction(ctypes.Structure):
	_fields_ = [
		("opcode", ctypes.c_int), # enum MOJOSHADER_preshaderOpcode
		("element_count", ctypes.c_uint),
		("operand_count", ctypes.c_uint),
		("operands", ctypes.POINTER(MojoShaderPreShaderOperand) * 4)
	]


class MojoShaderPreShader(ctypes.Structure):
	_fields_ = [
		("literal_count", ctypes.c_uint),
		("literals", ctypes.POINTER(ctypes.c_double)),
		("temp_count", ctypes.c_uint),
		("symbol_count", ctypes.c_uint),
		("symbols", ctypes.POINTER(MojoShaderSymbol)),
		("instruction_count", ctypes.c_uint),
	]


class MojoShaderParseData(ctypes.Structure):
	_fields_ = [
		("error_count", ctypes.c_int),
		("errors", ctypes.POINTER(MojoShaderError)),
		("profile", ctypes.c_char_p),
		("output", ctypes.POINTER(ctypes.c_char)),
		("output_len", ctypes.c_int),
		("instruction_count", ctypes.c_int),
		("shader_type", ctypes.c_int), # enum MOJOSHADER_shaderType
		("major_ver", ctypes.c_int),
		("minor_ver", ctypes.c_int),
		("mainfn", ctypes.c_char_p),
		("uniform_count", ctypes.c_int),
		("uniforms", ctypes.POINTER(MojoShaderUniform)),
		("constant_count", ctypes.c_int),
		("constants", ctypes.POINTER(MojoShaderConstant)),
		("sampler_count", ctypes.c_int),
		("samplers", ctypes.POINTER(MojoShaderSampler)),
		("attribute_count", ctypes.c_int),
		("attributes", ctypes.POINTER(MojoShaderAttribute)),
		("output_count", ctypes.c_int),
		("outputs", ctypes.POINTER(MojoShaderAttribute)),
		("swizzle_count", ctypes.c_int),
		("swizzles", ctypes.POINTER(MojoShaderSwizzle)),
		("symbol_count", ctypes.c_int),
		("symbols", ctypes.POINTER(MojoShaderSymbol)),
		("preshader", ctypes.POINTER(MojoShaderPreShader)),
		("malloc", ctypes.c_void_p),# MOJOSHADER_malloc malloc,
		("free", ctypes.c_void_p),# MOJOSHADER_free free,
		("malloc_data", ctypes.c_void_p)
	]


def load_lib(*names):
	for name in names:
		try:
			libname = ctypes.util.find_library(name)
			if libname:
				return ctypes.CDLL(libname)
			else:
				dll_path = os.path.join(os.getcwd(), "lib%s.dll" % (name))
				return ctypes.CDLL(dll_path)
		except OSError as e:
			print("Error", e)
	raise LibraryNotFoundException("Could not load the library %r" % (names[0]))


mojo = load_lib('mojoshader')
mojo.MOJOSHADER_parse.argtypes = [
	ctypes.c_char_p,
	ctypes.c_char_p,
	ctypes.POINTER(ctypes.c_char),
	ctypes.c_uint,
	ctypes.POINTER(MojoShaderSwizzle),
	ctypes.c_uint,
	ctypes.POINTER(MojoShaderSamplerMap),
	ctypes.c_uint,
	ctypes.c_void_p, # MOJOSHADER_malloc
	ctypes.c_void_p, # MOJOSHADER_free
    ctypes.c_void_p
]
mojo.MOJOSHADER_parse.restype = MojoShaderParseData

m = mojo.MOJOSHADER_parse("glsl", "main", b"\xff", 0, None, 0, None, 0, 0, 0, None)
print(m.profile, m.error_count, m.output_len)
