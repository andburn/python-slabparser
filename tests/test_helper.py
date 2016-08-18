import os
import io
import shaderlab


def read_data(file, mode="rb"):
	with open(os.path.join("tests", "data", file), mode) as f:
		return f.read()


def read_text_data(file):
	return read_data(file, "r")


def count_tokens_by_type(tokens):
	types = {}
	for t in tokens:
		key = t.type
		if t.value in shaderlab.keywords:
			key = "KEYWORD"
		if key not in types:
			types[key] = 0
		types[key] += 1
	return types
