import ply.yacc as yacc
import shaderlab_lex

tokens = shaderlab_lex.tokens

def p_program(p):
	'''program : section'''
	p[0] = p[1]

def p_section(p):
	'''section : title block content
			   | title block'''
	if len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1] + p[2]

def p_block(p):
	'''block : LBRACE content RBRACE
	         | LBRACE RBRACE'''
	if len(p) == 4:
		p[0] = '{ ' + p[2] + ' }'
	else:
		p[0] = '{}'

def p_content(p):
	'''content : section
	           | property
			   | STRING'''
	p[0] = p[1]

def p_property(p):
	'''property : IDENT LPAREN STRING COMMA keyword RPAREN EQUALS propvalue
				| IDENT LPAREN STRING COMMA keyword RPAREN EQUALS propvalue content
				| STRING EQUALS STRING
				| STRING EQUALS STRING content
				| keyword propvalue
				| keyword propvalue content
				| IDENT propvalue
				| IDENT propvalue content'''
	if len(p) == 3:
		p[0] = p[1] + '=' + str(p[2])
	elif len(p) == 4:
		p[0] = p[1] + '=' + p[3]
	elif len(p) == 5:
		p[0] = p[1] + '=' + p[3] + p[4]
	elif len(p) == 9:
		p[0] = p[1] + '=' + str(p[8])
	else:
		p[0] = p[1] + '=' + str(p[8]) + p[9]

def p_propvalue(p):
	'''propvalue : STRING LBRACE RBRACE
                 | STRING
	             | NUMBER
				 | vector'''
	p[0] = p[1]

def p_keyword(p):
	'''keyword : SHADER
	           | PROPERTIES
	           | SUBSHADER
	           | PASS
	           | TAGS
	           | FOG
	           | PROGRAM
	           | SUBPROGRAM
	           | KEYWORDS
	           | BIND
	           | MATRIX
	           | VECTOR
	           | FLOAT
	           | FALLBACK
	           | 2D
	           | COLOR'''
	p[0] = p[1]

def p_vector(p):
	'''vector : LPAREN NUMBER COMMA NUMBER COMMA NUMBER COMMA NUMBER RPAREN'''
	p[0] = '(vector)'

def p_title(p):
	'''title : keyword STRING
	         | keyword'''
	if len(p) == 3:
		p[0] = p[1] + '[' + p[2] + ']'
	else:
		p[0] = p[1]

def p_error(p):
    print("Syntax error in input! {}".format(p))

# Build the parser
parser = yacc.yacc(debug=True)

def parse(data):
	return parser.parse(data)
