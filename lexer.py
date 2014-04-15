# ------------------------------------------------------------
# lexer.py - Code to extract the tokens
#
# A compiler for converting the C language into Java Byte Code.
# Done as a part of project of course CS335.
#
# Authors-
# Prashant Jalan
# Arihant Kumar Jain
# Bhavishya Mittal
# Javesh Garg
# ------------------------------------------------------------

import ply.lex as lex
import sys

# List of token names. This is always required
tokens = ( 'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE', 'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG', 'REGISTER', 'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE', 'IDENTIFIER', 'HEX_NUM', 'EXP_NUM', 'REAL_NUM', 'INT_NUM', 'STRING', 'CHARACTER', 'ELLIPSIS', 'RIGHT_ASSIGN', 'LEFT_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN', 'RIGHT_OP', 'LEFT_OP', 'INC_OP', 'DEC_OP', 'PTR_OP', 'AND_OP', 'OR_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 'SEMICOLON', 'LEFT_CURL', 'RIGHT_CURL', 'COMMA', 'COLON', 'EQUAL', 'LEFT_ROUND', 'RIGHT_ROUND', 'LEFT_SQUARE', 'RIGHT_SQUARE', 'DOT', 'AMPERSAND', 'EXCLAMATION', 'TILDA', 'MINUS', 'PLUS', 'MULTIPLY', 'DIVIDE', 'MODULO', 'L_OP', 'G_OP', 'POWER', 'PIPE', 'QUESTION', 'HASH', 'COMMENT', 'COMMENTS', 'HEADER', 'PRINT')

# Regular expression rules for KEYWORDS
def t_AUTO(t):		r'auto'; return t
def t_BREAK(t):		r'break'; return t
def t_CASE(t):		r'case'; return t
def t_CHAR(t):		r'char'; return t
def t_CONST(t):		r'const'; return t
def t_CONTINUE(t):	r'continue'; return t
def t_DEFAULT(t):	r'default'; return t
def t_DO(t):		r'do'; return t
def t_DOUBLE(t):	r'double'; return t
def t_ELSE(t):		r'else'; return t
def t_ENUM(t):		r'enum'; return t
def t_EXTERN(t):	r'extern'; return t
def t_FLOAT(t):		r'float'; return t
def t_FOR(t):		r'for'; return t
def t_GOTO(t):		r'goto'; return t
def t_IF(t):		r'if'; return t
def t_INT(t):		r'int'; return t
def t_LONG(t):		r'long'; return t
def t_REGISTER(t):	r'register'; return t
def t_RETURN(t):	r'return'; return t
def t_SHORT(t):		r'short'; return t
def t_SIGNED(t):	r'signed'; return t
def t_SIZEOF(t):	r'sizeof'; return t
def t_STATIC(t):	r'static'; return t
def t_STRUCT(t):	r'struct'; return t
def t_SWITCH(t):	r'switch'; return t
def t_TYPEDEF(t):	r'typedef'; return t
def t_UNION(t):		r'union'; return t
def t_UNSIGNED(t):	r'unsigned'; return t
def t_VOID(t):		r'void'; return t
def t_VOLATILE(t):	r'volatile'; return t
def t_WHILE(t):		r'while'; return t
def t_PRINT(t):		r'print'; return t


# Regular expression rules for IDENTIFIERS
t_IDENTIFIER = r'[a-zA-Z_]([a-zA-Z0-9_])*'

# Regular expression rules for CONSTANTS
def t_HEX_NUM(t):	r'0(x|X)[0-9a-fA-F]+(uL|UL|ul|Ul|lu|lU|Lu|LU|l|L|u|U)?'; return t
def t_EXP_NUM(t):	r'((\d*\.\d+)|(\d+\.\d*)|\d+)(e|E)(\+|-)?\d+(l|L|f|F)?'; return t
def t_REAL_NUM(t):	r'(\d*\.\d+)|(\d+\.\d*)(f|F|l|L)?'; return t
def t_INT_NUM(t):	r'\d+(uL|UL|ul|Ul|lu|lU|Lu|LU|l|L|u|U)?'; return t
def t_STRING(t):	r'".*"'; return t
def t_CHARACTER(t):	r"'(\\.|[^\\'])'"; return t

# Regular expression rules for COMMENTS
def t_COMMENT(t):
	r'//.*'
	
def t_COMMENTS(t):
	r'/\*(.|\n)*\*/'

# Regular expression rules for HEADER FILES
def t_HEADER(t):
	#Compiler will return error
	r'\#[ \t]*include[ \t]*<.*>'
	sys.stdout.write("At Line "+str(t.lineno)+": ")
	print "Header file not supported"
	t.lexer.skip(1)

# Regular expression rules for OPERATORS & SPECIAL SYMBOLS
t_ELLIPSIS		= "\.\.\."
t_RIGHT_ASSIGN	= ">>="
t_LEFT_ASSIGN	= "<<="
t_ADD_ASSIGN	= "\+="
t_SUB_ASSIGN	= "-="
t_MUL_ASSIGN	= "\*="
t_DIV_ASSIGN	= "/="
t_MOD_ASSIGN	= "%="
t_AND_ASSIGN	= "&="
t_XOR_ASSIGN	= "\^="
t_OR_ASSIGN		= "\|="
t_RIGHT_OP		= ">>"
t_LEFT_OP		= "<<"
t_INC_OP		= "\+\+"
t_DEC_OP		= "--"
t_PTR_OP		= "->"
t_AND_OP		= "&&"
t_OR_OP			= "\|\|"
t_LE_OP			= "<="
t_GE_OP			= ">="
t_EQ_OP			= "=="
t_NE_OP			= "!="
t_SEMICOLON		= ";"
t_LEFT_CURL		= r'(\{|<%)'
t_RIGHT_CURL 	= r'(\}|%>)'
t_COMMA 		= ","
t_COLON 		= ":"
t_EQUAL 		= "="
t_LEFT_ROUND 	= "\("
t_RIGHT_ROUND	= "\)"
t_LEFT_SQUARE	= r'(\[|<:)'
t_RIGHT_SQUARE	= r'(\]|:>)'
t_DOT 			= "\."
t_AMPERSAND		= "&"
t_EXCLAMATION 	= "!"
t_TILDA 		= "~"
t_MINUS 		= "-"
t_PLUS			= "\+"
t_MULTIPLY		= "\*"
t_DIVIDE 		= "/"
t_MODULO		= "%"
t_L_OP 			= "<"
t_G_OP 			= ">"
t_POWER			= "\^"
t_PIPE			= "\|"
t_QUESTION 		= "\?"
t_HASH			= "\#"

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\v\f\r'

# Error handling rule
def t_error(t):
	sys.stdout.write("At Line "+str(t.lineno)+": ")
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)
	
# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Build the lexer
lexer = lex.lex()
	
def myLexer():
	#Take input from the user
	if len(sys.argv)>1:
		data = sys.argv[1]
	else:
		data = raw_input('Enter a file path: ')

	# Give the lexer some input
	lexer.input(open(data).read())

	# Tokenize
	while True:
		tok = lexer.token()
		if not tok:
			break      # No more input
		sys.stdout.write('('+tok.type+', "'+tok.value+'")\n')


if __name__ == "__main__":
	myLexer()
