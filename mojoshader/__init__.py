import ctypes
from ctypes import Structure, Union, POINTER


class Error(Structure):
	_fields_ = [
		("error", ctypes.c_char_p),
		("filename", ctypes.c_char_p),
		("error_position", ctypes.c_int)
	]


class Swizzle(Structure):
	_fields_ = [
		("usage", ctypes.c_int), # enum MOJOSHADER_usage
		("index", ctypes.c_int),
		("swizzles", ctypes.c_char * 4)
	]


class Uniform(Structure):
	_fields_ = [
		("type", ctypes.c_int), # enum MOJOSHADER_uniformType
		("index", ctypes.c_int),
		("array_count", ctypes.c_int),
		("constant", ctypes.c_int),
		("name", ctypes.c_char_p)
	]


class ConstantUniform(Union):
	_fields_ = [
		("f", ctypes.c_float * 4),
		("i", ctypes.c_int * 4),
		("b", ctypes.c_int),
	]


class Constant(Structure):
	_fields_ = [
		("type", ctypes.c_int), # enum MOJOSHADER_uniformType
		("index", ctypes.c_int),
		("value", ConstantUniform)
	]


class Sampler(Structure):
	_fields_ = [
		("type", ctypes.c_int), # enum MOJOSHADER_samplerType
		("index", ctypes.c_int),
		("name", ctypes.c_char_p),
		("texbem", ctypes.c_int)
	]


class SamplerMap(Structure):
	_fields_ = [
		("index", ctypes.c_int),
		("type", ctypes.c_int), # enum MOJOSHADER_samplerType
	]


class Attribute(Structure):
	_fields_ = [
		("usage", ctypes.c_int), # enum MOJOSHADER_usage
		("index", ctypes.c_int),
		("name", ctypes.c_char_p)
	]


class SymbolTypeInfo(Structure):
	_fields_ = [
		("parameter_class", ctypes.c_int), # enum MOJOSHADER_symbolClass
		("parameter_type", ctypes.c_int), # enum MOJOSHADER_symbolType
		("rows", ctypes.c_uint),
		("columns", ctypes.c_uint),
		("elements", ctypes.c_uint),
		("member_count", ctypes.c_uint)
	]


class SymbolStructMember(Structure):
	_fields_ = [
		("name", ctypes.c_char_p),
		("info", POINTER(SymbolTypeInfo))
	]


class Symbol(Structure):
	_fields_ = [
		("name", ctypes.c_char_p),
		("register_set", ctypes.c_int), # enum MOJOSHADER_symbolRegisterSet
		("register_index", ctypes.c_uint),
		("register_count", ctypes.c_uint),
		("info", POINTER(SymbolTypeInfo)),
	]


class PreShaderOperand(Structure):
	_fields_ = [
		("type", ctypes.c_int), # enum MOJOSHADER_preshaderOperandType
		("index", ctypes.c_uint),
		("array_register_count", ctypes.c_uint),
		("array_registers", POINTER(ctypes.c_uint))
	]


class PreShaderInstruction(Structure):
	_fields_ = [
		("opcode", ctypes.c_int), # enum MOJOSHADER_preshaderOpcode
		("element_count", ctypes.c_uint),
		("operand_count", ctypes.c_uint),
		("operands", POINTER(PreShaderOperand) * 4)
	]


class PreShader(Structure):
	_fields_ = [
		("literal_count", ctypes.c_uint),
		("literals", POINTER(ctypes.c_double)),
		("temp_count", ctypes.c_uint),
		("symbol_count", ctypes.c_uint),
		("symbols", POINTER(Symbol)),
		("instruction_count", ctypes.c_uint),
	]


class ParseData(Structure):
	_fields_ = [
		("error_count", ctypes.c_int),
		("errors", POINTER(Error)),
		("profile", ctypes.c_char_p),
		("output", POINTER(ctypes.c_char)),
		("output_len", ctypes.c_int),
		("instruction_count", ctypes.c_int),
		("shader_type", ctypes.c_int), # enum MOJOSHADER_shaderType
		("major_ver", ctypes.c_int),
		("minor_ver", ctypes.c_int),
		("mainfn", ctypes.c_char_p),
		("uniform_count", ctypes.c_int),
		("uniforms", POINTER(Uniform)),
		("constant_count", ctypes.c_int),
		("constants", POINTER(Constant)),
		("sampler_count", ctypes.c_int),
		("samplers", POINTER(Sampler)),
		("attribute_count", ctypes.c_int),
		("attributes", POINTER(Attribute)),
		("output_count", ctypes.c_int),
		("outputs", POINTER(Attribute)),
		("swizzle_count", ctypes.c_int),
		("swizzles", POINTER(Swizzle)),
		("symbol_count", ctypes.c_int),
		("symbols", POINTER(Symbol)),
		("preshader", POINTER(PreShader)),
		("malloc", ctypes.c_void_p),# MOJOSHADER_malloc malloc,
		("free", ctypes.c_void_p),# MOJOSHADER_free free,
		("malloc_data", ctypes.c_void_p)
	]
