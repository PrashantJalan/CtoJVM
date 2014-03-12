import sys
from lexer import tokens
import ply.yacc as yacc


#Grammar definitions

def p_program_1(t):
	'program : program function'
	pass

def p_program_2(t):
	'program : function'
	pass

def p_function_1(t):
	'function : functionDeclaration'
	pass
'''
def p_function_2(t):    
	'function : functionDefinition'
	pass
'''
def p_functionDeclaration_1(t):
	'functionDeclaration : functionReturnType functionName argumentList SEMICOLON'
	pass

def p_functionReturnType_1(t):
	'functionReturnType : dataType'
	pass

def p_dataType_1(t):
	'''
	dataType  : VOID
		  | CHAR
                  | SHORT
                  | INT
                  | LONG
                  | FLOAT
                  | DOUBLE
                  | SIGNED
                  | UNSIGNED 
	'''
	pass

def p_functionName_1(t):
	'functionName : IDENTIFIER'
	pass

def p_argumentList_1(t):
	'argumentList : LEFT_ROUND arguments RIGHT_ROUND'
	pass

def p_arguments_1(t):
	'arguments : arguments COMMA oneArgument'
	pass

def p_arguments_2(t):
	'arguments : oneArgument'
	pass

def p_oneArgument_1(t):
	'oneArgument : dataType IDENTIFIER'
	pass

def p_oneArgument_2(t):
	'oneArgument : dataType IDENTIFIER EQUAL value'
	pass

def p_value_1(t):
	'''value : HEX_NUM
		 | INT_NUM
		 | EXP_NUM
		 | REAL_NUM'''	
	pass

def p_error(p):
    print "Syntax error in input!"


# Build the parser
parser = yacc.yacc()

def myParser():
	#Debugging purposes

	#Take input from the user
	if len(sys.argv)>1:
		data = sys.argv[1]
	else:
		data = raw_input('Enter a file path: ')

	ast = parser.parse(open(data).read())
	print ast


if __name__=='__main__':
	myParser()