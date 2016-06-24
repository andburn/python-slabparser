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


	def __repr__(self):
		return 'Shader({})'.format(self.name)


class Property:
	def __init__(self, name, pair, value):
		self.name = name
		self.long_name = pair[0]
		self.type = pair[1]
		self.value = value

	def __repr__(self):
		return 'Property({}, {}) = {}'.format(self.name, self.type, self.value)


class Pair:
	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __repr__(self):
		return 'Pair({},{})'.format(self.key, self.value)

class SubShader:
	def __init__(self, sections):
		self.sections = sections
		# merge dicts
		merged = {}
		for s in sections:
			if isinstance(s, dict):
				merged.update(s)

		self.passes = merged.get('passes')
		self.tags = merged.get('tags')

	def __repr__(self):
		return 'SubShader() {}'.format(self.sections)


class Pass:
	def __init__(self, sections):
		self.sections = sections
		# merge dicts
		merged = {}
		for s in sections:
			if isinstance(s, dict):
				merged.update(s)

		self.name = merged.get('name')
		self.tags = merged.get('tags')
		self.fog = merged.get('fog')
		self.bind = merged.get('bind')

	def __repr__(self):
		return 'Pass()'

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
