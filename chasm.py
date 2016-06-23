import sys
import shaderlab_lex
import shaderlab_parse


def main():
	if len(sys.argv) != 2:
		print('Usage: chasm.py <file>')
		sys.exit(2)

	with open(sys.argv[1], 'r') as f:
	    data = f.read()

	# show data as lexed tokens
	for t in shaderlab_lex.tokenize(data):
		print(t)

	# show parse data
	print(shaderlab_parse.parse(data))


if __name__ == "__main__":
	main()
