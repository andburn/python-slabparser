import pytest
import shaderlab
from test_helper import *


def test_basic():
	'''Test on a basic compilied shader, equivalent to Unity 5.2 and below'''
	shader = read_text_data("basic.shader")
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


def test_uber():
	'''Test lexer on an uber compilied shader, equivalent to Unity 5.2 and below'''
	shader = read_text_data("uber.shader")
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


def test_stripped():
	'''Test on a uber compilied shader, equivalent to Unity 5.3 '''
	shader = read_text_data("stripped.shader")
	tokens = shaderlab.tokenize(shader)
	types = count_tokens_by_type(tokens)
	assert types["STRING"] == 21
	assert types["NUMBER"] == 15
	assert types["LBRACE"] == 14
	assert types["RBRACE"] == 14
	assert types["IDENT"] == 9
	assert types["LPAREN"] == 4
	assert types["RPAREN"] == 4
	assert types["COMMA"] == 8
	assert types["EQUALS"] == 6
	assert types["KEYWORD"] == 18
	assert "LBRACKET" not in types
	assert "RBRACKET" not in types
