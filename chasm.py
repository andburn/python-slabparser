import re
import sys

ins_re = r'^([a-z0-9_]+)\s*(.+)?$'
keywords_re = r'^Keywords { (.*) }'
uniforms_re = r'(Float|Vector|Matrix|SetTexture)\s+(\d+)\s+\[(.*)\]'

class Vec(object):
	def __init__(self, arg):
		m = re.match(r'([a-zA-Z]+\d+)\.?([xywz]+)?', arg)
		if m:
			self.name = m.group(1)
			self.swizzle = m.group(2)

	def get_type(self):
		if (self.swizzle):
			swiz_len = len(self.swizzle)
			if (swiz_len == 1):
				return "float"
			elif (swiz_len == 2):
				return "vec2"
			elif (swiz_len == 3):
				return "vec3"
			elif (swiz_len == 4):
				return "vec4"
		else:
			return "vec4"


def uniforms(constants, type, number, name):
	if number in constants:
		print("ERROR: %s duplicated constant" % (number))
	else:
		constants[int(number)] = name

	if type == 'Float':
		print("uniform float %s;" % name)
	elif type == 'Vector':
		print("uniform vec4 %s;" % name)
	elif type == 'Matrix':
		print("uniform mat4 %s;" % name)
	elif type == 'SetTexture':
		print("uniform sampler2D %s;" % name)
	else:
		print("UNKNOWN: %s" % (type, number, name))


def write_ins(dest, lhs):
	d = Vec(dest)
	return "%s = %s(%s);" % (dest, d.get_type(), lhs)


# TODO r0_abs
def instruction(ins, args):
	out = "unknown"
	regs = []
	if args:
		regs = args.split(', ')

	if ins == 'add' or ins == 'add_pp':
		out = write_ins(regs[0], "%s + %s" % tuple(regs[1:]))
	elif ins == 'add_sat' or ins == 'add_sat_pp':
		out = write_ins(regs[0], "clamp(%s + %s, 0.0, 1.0)" % tuple(regs[1:]))
	elif ins == 'mad' or ins == 'mad_pp':
		out = write_ins(regs[0], "%s * %s + %s" % tuple(regs[1:]))
	elif ins == 'mad_sat' or ins == 'mad_sat_pp':
		out = write_ins(regs[0], "clamp(%s * %s + %s, 0.0, 1.0)" % tuple(regs[1:]))
	elif ins == 'mul' or ins == 'mul_pp':
		out = write_ins(regs[0], "%s * %s" % tuple(regs[1:]))
	elif ins == 'mul_sat':
		out = write_ins(regs[0], "clamp(%s * %s, 0.0, 1.0)" % tuple(regs[1:]))
	elif ins == 'mov' or ins == 'mov_pp':
		out = write_ins(regs[0], "%s" % tuple(regs[1:]))
	elif ins == 'mov_sat' or ins == 'mov_sat_pp':
		out = write_ins(regs[0], "clamp(%s, 0.0, 1.0)" % tuple(regs[1:]))
	elif ins == 'frc':
		out = write_ins(regs[0], "fract(%s)" % tuple(regs[1:]))
	elif ins == 'slt':
		out = write_ins(regs[0], "%s < %s ? 1.0 : 0.0" % tuple(regs[1:]))
	elif ins == 'sincos':
		r = Vec(regs[0])
		if 'x' in r.swizzle:
			out = write_ins("%s.x" % (r.name), "cos(%s)" % tuple(regs[1:]))
		if 'y' in r.swizzle:
			out = write_ins("%s.y" % (r.name), "sin(%s)" % tuple(regs[1:]))
	elif ins == 'lrp' or ins == 'lrp_pp':
		out = write_ins(regs[0], "%s * (%s - %s) + %s" % (regs[1], regs[2], regs[3], regs[3]))
	elif ins == 'else':
		out = "} else {"
	elif ins == 'if_ne':
		out = "if (%s != %s) {" % tuple(regs)
	elif ins == 'if_lt':
		out = "if (%s < %s) {" % tuple(regs)
	elif ins == 'if_gt':
		out = "if (%s > %s) {" % tuple(regs)
	elif ins == 'endif':
		out = "}"
	elif ins == 'def':
		out = "%s = vec4(%s, %s, %s, %s);" % tuple(regs)
	elif ins == 'cmp':
		d = Vec(regs[0])
		out = "%s = %s >= 0.0 ? %s(%s) : %s(%s);" % (regs[0], regs[1], d.get_type(), regs[2], d.get_type(), regs[3])
	elif ins == 'min' or ins == 'min_pp':
		# assuming glsl min is same
		out = write_ins(regs[0], "min(%s, %s)" % (regs[1],regs[2]))
	elif ins == 'texld' or ins == 'texld_pp':
		out = "%s = texture2D(%s, vec2(%s));" % (regs[0], regs[2], regs[1])
	else:
		out = "UNKNOWN: %s %s" % (ins, regs)

	return out


def parse_line(line):
	out = line
	res = re.match(ins_re, line)
	if res:
		out = instruction(res.group(1), res.group(2))
	return out


def parse_file(file):
	shader_flag = False
	with open(file) as f:
		for line in f.readlines():
			begin = re.match('\"(p|v)s', line)
			if begin:
				if begin.group(1) == 'v':
					print('// Vertex')
				else:
					print('// Pixel')
				shader_flag = True
				continue
			if re.match('\"$', line):
				shader_flag = False
				print('// End')
			if shader_flag and line.strip():
				print(parse_line(line))


def main():
	if len(sys.argv) != 2:
		print("usage: chasm.py <file>")
		sys.exit(2)
	try:
		parse_file(sys.argv[1])
	except FileNotFoundError as e:
		print(e)
		sys.exit(1)
	except EnvironmentError as e:
		print(e)
		sys.exit(1)


if __name__ == "__main__":
	main()
