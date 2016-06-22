import ply.lex as lex
import ply.yacc as yacc

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
	'2D'
)


t_LBRACE    = r'{'
t_RBRACE    = r'}'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMMA     = r','
t_EQUALS    = r'='
t_STRING   = r'".*?"'
#t_NUMBER   = r'\d+'
t_IDENT = r'[A-Za-z_0-9]+'

def t_2D(t):
	r'2D'
	return t

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# Test it out
data = '''
Shader "Custom/Card/GoldenPortraitUber" {
Properties {
 _MainTex ("Portrait (RGB)", 2D) = "black" { }
 _Fx1_Color ("FX1 Color", Color) = (1,1,1,1)
 _Fx1_Intensity ("FX1 Intensity", Float) = 1
}
SubShader {
 Tags { "RenderType"="Opaque" "Highlight"="true" }
 Pass {
  Name "CARDUBER"
  Tags { "RenderType"="Opaque" "Highlight"="true" }
  Fog {
   Color (0,0,0,1)
  }
  GpuProgramID 4477
  }
}
}
'''
simpler = '''
Shader "Custom/Card/GoldenPortraitUber" {
SubShader {
 Tags {  }
 Pass {
  }
}
}
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

# define parser

def p_program(p):
	'program : section'
	p[0] = p[1]

def p_title_single(p):
	'title : IDENT'
	p[0] = p[1]

def p_title_text(p):
	'title : IDENT STRING'
	p[0] = p[1]

def p_section_empty(p):
	'section : title LBRACE RBRACE'
	p[0] = p[1]

def p_section_nested(p):
	'section : title LBRACE section RBRACE'
	p[0] = p[1]

def p_error(p):
    print("Syntax error in input! {}".format(p))

# Build the parser
parser = yacc.yacc()

result = parser.parse(simpler)
print(result)
