from enum import IntEnum

keywords = {
	"Shader": "SHADER",
	"Properties": "PROPERTIES",
	"SubShader": "SUBSHADER",
	"Pass": "PASS",
	"Tags": "TAGS",
	"Fog": "FOG",
	"Program": "PROGRAM",
	"SubProgram": "SUBPROGRAM",
	"Keywords": "KEYWORDS",
	"Bind": "BIND",
	"Matrix": "MATRIX",
	"Vector": "VECTOR",
	"Float": "FLOAT",
	"Fallback": "FALLBACK",
	"CustomEditor": "CUSTOMEDITOR",
	"2D": "2D",
	"Color": "COLOR",
	"Off": "OFF",
	"BindChannels": "BINDCHANNELS",
	"Vertex": "VERTEX",
	"TexCoord": "TEXCOORD",
	"TexCoord0": "TEXCOORD0",
	"TexCoord1": "TEXCOORD1",
	"Name": "NAME",
	"Range": "RANGE"
}


class ProgramType(IntEnum):
	VERTEX = 0
	FRAGMENT = 1


class ProgramFormat(IntEnum):
	OPENGL = 0
	D3D9 = 1
	D3D11 = 2


class Pair:
	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __repr__(self):
		return 'Pair({},{})'.format(self.key, self.value)


class RegisterEntry:
	def __init__(self, name, position, type):
		self.name = name
		self.position = int(position)
		self.type = type

	def __repr__(self):
		return '[{}] {} {}'.format(self.position, self.type, self.name)


class Shader:
	def __init__(self, name, sections):
		self.name = name
		self.sections = sections

		# merge dicts
		merged = {}
		for s in sections:
			if isinstance(s, dict):
				merged.update(s)

		self.properties = merged.get('props')
		self.fallback = merged.get('fallback')
		self.custom_editor = merged.get('customed')
		self.subshaders = [merged.get('subshaders')]

	@property
	def vertex_programs(self):
		return self._shader_programs(ProgramType.VERTEX)

	@property
	def fragment_programs(self):
		return self._shader_programs(ProgramType.FRAGMENT)

	def _shader_programs(self, ptype):
		v = []
		# TODO must be a better way than this
		for ss in self.subshaders:
			for ps in ss.passes:
				for pg in ps.programs:
					if pg.type == ptype:
						v = pg.subprograms
		return v

	def __repr__(self):
		return 'Shader({})'.format(self.name)


# TODO types should be acutal types/classes
class Property:
	def __init__(self, name, pair, value):
		self.name = name
		self.description = pair[0]
		self.type = pair[1]
		self.value = value

	def __repr__(self):
		return 'Property({}, {}) = {}'.format(self.name, self.type, self.value)


class SubShader:
	def __init__(self, sections):
		self.sections = sections
		self.tags = []
		self.passes = []

		for s in sections:
			if isinstance(s, list) and len(s) > 0 and isinstance(s[0], Pair):
				self.tags += s
			elif isinstance(s, Pass):
				self.passes.append(s)

	def __repr__(self):
		return 'SubShader() {}'.format(self.sections)


class Pass:
	def __init__(self, sections):
		self.sections = sections
		self.programs = []
		self.state = []
		# merge dicts
		merged = {}
		for s in sections:
			if isinstance(s, dict):
				merged.update(s)
			elif isinstance(s, Program):
				self.programs.append(s)
			elif isinstance(s, Pair):
				self.state.append(s)

		self.name = merged.get('name')
		self.tags = merged.get('tags')
		self.fog = merged.get('fog')
		self.bind = merged.get('bind')

	def __repr__(self):
		return 'Pass() {}'.format(self.sections)


class Program:
	def __init__(self, type, subprograms):
		self.subprograms = subprograms
		if type == 'vp':
			self.type = ProgramType.VERTEX
		elif type == 'fp':
			self.type = ProgramType.FRAGMENT
		else:
			raise ValueError("{} must be either 'vp' or 'fp'".format(type))

	def __repr__(self):
		return 'Program({})'.format(self.type)


class SubProgram:
	def __init__(self, format, sections):
		self.sections = sections
		fmt = format.strip().lower()
		if fmt == "d3d9":
			self.format = ProgramFormat.D3D9
		elif fmt == "d3d11":
			self.format = ProgramFormat.D3D11
		elif fmt == "opengl":
			self.format = ProgramFormat.OPENGL
		else:
			raise NotImplementedError("{} is an unknown format".format(format))

		self.code = None
		self.constants = []
		self.defs = []
		self.keywords = []
		for s in sections:
			if isinstance(s, Pair):
				self.defs.append(s)
			elif isinstance(s, RegisterEntry):
				self.constants.append(s)
			elif isinstance(s, list):
				self.keywords = s
			elif isinstance(s, str):
				self.code = s

	def __repr__(self):
		return 'SubProgram({})'.format(self.format)


class FallBack:
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return 'Fallback({})'.format(self.value)


class CustomEditor:
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return 'CustomEditor({})'.format(self.value)
