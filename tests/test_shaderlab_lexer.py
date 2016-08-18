import pytest
import shaderlab
from test_helper import *


def test_basic_5_1():
	'''Test on a basic compilied shader, equivalent to Unity 5.2 and below'''
	shader = read_text_data("basic_5.1.shader")
	tokens = shaderlab.tokenize(shader)
	types = count_tokens_by_type(tokens)
	assert types["STRING"] == 20
	assert types["NUMBER"] == 9
	assert types["LBRACE"] == 12
	assert types["RBRACE"] == 12
	assert types["IDENT"] == 6
	assert types["LPAREN"] == 3
	assert types["RPAREN"] == 3
	assert types["COMMA"] == 5
	assert types["EQUALS"] == 6
	assert types["LBRACKET"] == 2
	assert types["RBRACKET"] == 2
	assert types["KEYWORD"] == 19


def test_uber_5_1():
	'''Test lexer on an uber compilied shader, equivalent to Unity 5.2 and below'''
	shader = read_text_data("uber_5.1.shader")
	tokens = shaderlab.tokenize(shader)
	types = count_tokens_by_type(tokens)
	assert types["NUMBER"] == 26
	assert types["LBRACE"] == 18
	assert types["RBRACE"] == 18
	assert types["STRING"] == 41
	assert types["IDENT"] == 18
	assert types["LPAREN"] == 7
	assert types["RPAREN"] == 7
	assert types["COMMA"] == 11
	assert types["EQUALS"] == 8
	assert types["LBRACKET"] == 10
	assert types["RBRACKET"] == 10
	assert types["KEYWORD"] == 46
