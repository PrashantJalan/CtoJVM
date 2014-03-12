import sys
from lexer import tokens
import ply.yacc as yacc
import pydot
import os

#Printing AST; Debugging purpose

class Node:
	count  = 0
	type = 'Node(unspecified)'
	shape = 'ellipse'
	def __init__(self, type, children=None):
		self.ID = str(Node.count)
		self.type = type
		Node.count+=1
		if not children: self.children = []
		elif hasattr(children,'__len__'):
			self.children = children
		else:
			self.children = [children]
		self.next = []

	def makegraphicaltree(self, dot=None, edgeLabels=True):
		if not dot: dot = pydot.Dot()
		dot.add_node(pydot.Node(self.ID, label=self.type, shape=self.shape))
		label = edgeLabels and len(self.children)-1
		for i,c in enumerate(self.children):
			c.makegraphicaltree(dot, edgeLabels)
			edge = pydot.Edge(self.ID,c.ID)
			if label:
				edge.set_label(str(i))
			dot.add_edge(edge)
		return dot

#Grammar definitions
#start rule
def p_program_1(t):
	'program : program function'
	t[0] = Node('start',[t[1],t[2]])
	pass

def p_program_2(t):
	'program : function'
	t[0] = Node('function',[t[1]])
	pass

#function
def p_function_1(t):
	'function : functionDeclaration'
	t[0] = Node('funcDeclare',[t[1]])
	pass

#function declaration
def p_functionDeclaration_1(t):
	'functionDeclaration : functionReturnType functionName argumentList SEMICOLON'
	t[0] = Node('functionSyntax',[t[1],t[2],t[3],Node(t[4],[])])
	pass

def p_functionReturnType_1(t):
	'functionReturnType : dataType'
	t[0] = Node('dataType',[t[1]])
	pass

#data types
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
	t[0] = Node('type',[Node(t[1],[])])
	pass

def p_functionName_1(t):
	'functionName : IDENTIFIER'
	t[0] = Node('funcName',[Node(t[1],[])])
	pass

#arguments in function
def p_argumentList_1(t):
	'argumentList : LEFT_ROUND arguments RIGHT_ROUND'
	t[0] = Node('argumentList',[t[2]])
	pass

def p_argumentList_2(t):
	'argumentList : LEFT_ROUND RIGHT_ROUND'
	t[0] = Node('argumentList',[])
	pass

def p_arguments_1(t):
	'arguments : arguments COMMA oneArgument'
	t[0] = Node('argument',[t[1],t[3]])
	pass

def p_arguments_2(t):
	'arguments : oneArgument'
	t[0] = Node('argument',[t[1]])
	pass

def p_oneArgument_1(t):
	'oneArgument : dataType IDENTIFIER'
	t[0] = Node('argumentDeclare',[t[1],Node(t[2],[])])
	pass

def p_oneArgument_2(t):
	'oneArgument : dataType IDENTIFIER EQUAL value'
	t[0] = Node('argumentDeclare',[t[1],Node(t[2],[]),t[4]])
	pass

#Constant value
def p_value_1(t):
	'''value : HEX_NUM
		 | INT_NUM
		 | EXP_NUM
		 | REAL_NUM'''	
	pass
	t[0] = Node('value',[Node(t[1],[])])


def p_error(p):
	sys.stdout.write("At Line "+str(p.lineno)+": ")
	print "Syntax error at token", p.value
	yacc.errok()


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
	t = ast.makegraphicaltree()
	t.write_pdf('AST.pdf')

if __name__=='__main__':
	myParser()