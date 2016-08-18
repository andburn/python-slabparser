import ply.lex as lex
from .shaderlab import keywords


# define the lexical tokens, plus keywords
tokens = (
	"NUMBER",
	"LBRACE",
	"RBRACE",
	"STRING",
	"IDENT",
	"LPAREN",
	"RPAREN",
	"COMMA",
	"EQUALS",
	"LBRACKET",
	"RBRACKET"
) + tuple(keywords.values())


# Begin token regex definitions (order matters)
# STRING, double quoted multi-line strings
def t_STRING(t):
	r'"[\n_0-9a-zA-Z\-,\s\/\(\)\[\]\.]+"'
	t.value = t.value[1:-1]
	return t


# Single character tokens
t_LBRACE    = r'{'
t_RBRACE    = r'}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMMA     = r','
t_EQUALS    = r'='


# 2D, is a special case to avoid number/ident conflicts
def t_2D(t):
	r'2D'
	return t


# IDENT, identifiers not starting with a number, assign to keyword terminals
def t_IDENT(t):
	r'[A-Za-z_][A-Za-z_0-9]*'
	t.type = keywords.get(t.value, 'IDENT')
	return t


# NUMBER, ints and floats (without exp), convert to float type
def t_NUMBER(t):
	r'(-?(\d+(\.\d*)?|\.\d+))'
	t.value = float(t.value)
	return t


# NewLine, track line breaks to allow storing of line numbers
# TODO not used at the moment
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ignored characters (spaces and tabs)
t_ignore  = ' \t'


# lex error
# TODO could skip token with 't.lexer.skip(1)'
def t_error(t):
	raise lex.LexError("Illegal character '%s'" % t.value[0])


# Build the lexer
lexer = lex.lex(debug=False)


# Tokenize a string, mostly to allow testing
def tokenize(data):
	'''Use the defined lexer to return a list of tokens from data'''
	tokenized = []
	lexer.input(data)
	while True:
	    tok = lexer.token()
	    if not tok:
	        break
	    tokenized.append(tok)
	return tokenized
