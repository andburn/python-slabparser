from io import BytesIO
from .utils import BinaryReader

class Blob:
	def __init__(self, buf):
		self.buf = BinaryReader(BytesIO(buf))
		self.shaders = self.extract_shaders()

	def extract_shaders(self):
		subshaders = []
		tags = []
		index = []

		num_subprograms = self.buf.read_int()
		for i in range(num_subprograms):
			index.append((self.buf.read_int(), self.buf.read_int()))

		for offset, length in index:
			self.buf.seek(offset)
			data = self.buf.read(length)
			b = BinaryReader(BytesIO(data))
			# unknown, seems to be same for all shaders, unity id?
			sid = b.read_int()
			# shader type (9 = vs_2_0, 11 = ps_2_0)
			# TODO look for vs/ps_1 shaders to check
			stype = b.read_int()
			# unknown series of bytes (12)
			u2, u3, u4 = (b.read_int(), b.read_int(), b.read_int())
			# the number of associated shader keywords
			num_tags = b.read_int()
			# get the tag strings
			for t in range(num_tags):
				size = b.read_int()
				tags.append(b.read_string(size))
				b.align()
			# the length of the shader bytecode
			length = b.read_int()
			# read bytecode and combine with tags
			subshaders.append((tags, b.read(length)))
			# TODO some other stuff at the end, not sure yet
		return subshaders
