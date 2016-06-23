import ply.lex as lex


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
	"2D": "2D",
	"Color": "COLOR"
}

tokens = (
	'NUMBER',
	'LBRACE',
	'RBRACE',
	'STRING',
	'IDENT',
	'LPAREN',
	'RPAREN',
	'COMMA',
	'EQUALS',
	'LBRACKET',
	'RBRACKET'
) + tuple(keywords.values())


# double quoted multi-line strings
def t_STRING(t):
	r'"[\n_0-9a-zA-Z\-,\s\/\(\)\[\]\.]+"'
	return t


t_LBRACE    = r'{'
t_RBRACE    = r'}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMMA     = r','
t_EQUALS    = r'='


# special case, number/ident conflicts
def t_2D(t):
	r'2D'
	return t


# identifiers not starting with a number, assign to keyword terminals
def t_IDENT(t):
	r'[A-Za-z_][A-Za-z_0-9]*'
	t.type = keywords.get(t.value, 'IDENT')
	return t


# ints and floats (without exp), covert to float type
def t_NUMBER(t):
	r'(-?(\d+(\.\d*)?|\.\d+))'
	t.value = float(t.value)
	return t

# TODO not really necessary
# track line breaks for line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ignored characters (spaces and tabs)
t_ignore  = ' \t'


# TODO raise LexError?
# lex error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build lexer
lexer = lex.lex(debug=False)


def tokenize(data):
	tokenized = []
	lexer.input(data)
	while True:
	    tok = lexer.token()
	    if not tok:
	        break
	    tokenized.append(tok)
	return tokenized
