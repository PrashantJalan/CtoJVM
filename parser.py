import sys
from lexer import tokens
import ply.yacc as yacc
import pydot
import os

precedence = (
	('nonassoc', 'else_priority'),
	('nonassoc', 'ELSE'),
)

#Symbol Table
class SymbolTable:
    """A symbol table class. There is a separate symbol table for 
    each code element that has its own scope."""

    def __init__(self, parent=None):
        self.entries = {}
        self
        self.parent = parent
        if self.parent != None:
            self.parent.children.append(self)
        self.children = []
    
    def add(self, name, type, attribute=None, value=None):
    	#name, type and value are token objects 
        if self.entries.has_key(name.value):
            sys.stdout.write("At Line "+str(name.lineno)+": Variable "+name.value+" redefined.\n")
        else:
        	self.entries[name.value] = [value, type, attribute]

    def modify(self, name, value):
    	if self.entries.has_key(name.value):
    		self.entries[name.value][0] = value
    	else:
    		sys.stdout.write("At Line "+str(name.lineno)+": Variable "+name.value+" not declared.\n")

    def get(self, name):
        if self.entries.has_key(name.value):
            return self.entries[name.value]
        else:
            if self.parent != None:
                return self.parent.get(name.value)
            else:
                return None

#Tree Node for AST
class Node:
	count  = 0
	type = 'Node(unspecified)'
	shape = 'ellipse'
	def __init__(self, type, children=None):
		self.ID = str(Node.count)
		self.parent = None
		self.type = type
		Node.count+=1
		if not children: self.children = []
		elif hasattr(children,'__len__'):
			self.children = children
		else:
			self.children = [children]
		for it in children:
			it.parent = self
		self.next = []

	def add(self, t):
		#Adds t as a sibling
		self.children.append(t)

	def makegraphicaltree(self, dot=None, edgeLabels=True):
		if not dot: dot = pydot.Dot()
		customLabel = self.type
		if customLabel[0] == '"':
			customLabel = '\\' + customLabel
		if customLabel[-1] == '"':
			customLabel = customLabel[:-1] + '''\\"'''
		customLabel = '"'+customLabel+'"'
		dot.add_node(pydot.Node(self.ID, label=customLabel, shape=self.shape))
		label = edgeLabels and len(self.children)-1
		for i,c in enumerate(self.children):
			c.makegraphicaltree(dot, edgeLabels)
			edge = pydot.Edge(self.ID,c.ID)
			if label:
				edge.set_label(str(i))
			dot.add_edge(edge)
		return dot

currentSymbolTable = SymbolTable()

#Grammar definitions
start = 'program'

def p_program(t):
	'program : function_list'
	t[0] = t[1]

def p_function_list_1(t):
	'function_list : function_list function'
	t[1].add(t[2])
	t[0] = t[1]

def p_function_list_2(t):
	'function_list : function'
	t[0] = Node('function_list', [t[1]])

def p_function_1(t):
	'function : function_declaration'
	t[0] = t[1]

def p_function_2(t):
	'function : function_definition'
	t[0]=t[1]

def p_function_declaration(t):
	'function_declaration : return_type_specifier IDENTIFIER LEFT_ROUND argument_list RIGHT_ROUND SEMICOLON'
	t[0] = Node('function_declaration',[t[1], Node(t[2], []), t[4]])

def p_return_type_specifier_1(t):
	'return_type_specifier : type_specifier'
	t[0] = t[1]

def p_return_type_specifier_2(t):
	'return_type_specifier : VOID'
	t[0] = Node(t[1],[])

def p_type_specifier_1(t):
	'''type_specifier : CHAR
						| SHORT
						| INT 
						| LONG 
						| FLOAT 
						| DOUBLE 
						| SIGNED 
						| UNSIGNED'''
	t[0] = Node(t[1],[])

def p_argument_list_1(t):
	'argument_list : argument'
	t[0] = Node('argument_list',[t[1]])

def p_argument_list_2(t):
	'argument_list : argument_list COMMA argument'
	t[1].add(t[3])
	t[0] = t[1]

def p_argument_1(t):
	'argument : type_specifier IDENTIFIER'
	t[0]= Node('argument',[t[1], Node(t[2], [])])

def p_argument_2(t):
	'argument : type_specifier array'
	t[0]= Node('argument',[t[1], t[2]])

def p_function_definition(t):
	'function_definition : return_type_specifier IDENTIFIER LEFT_ROUND argument_list RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL'
	t[0] = Node('function_definition', [t[1], Node(t[2], []), t[4], t[7]])

def p_statement_list_1(t):
	'statement_list : statement_list statement'
	t[1].add(t[2])
	t[0] = t[1]

def p_statement_list_2(t):
	'statement_list : statement'
	t[0] = Node('statement_list', [t[1]])
'''
def p_statement_1(t):
	'statement : assignment_statement'
	t[0] = t[1]
'''
def p_statement_2(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL %prec else_priority'
	t[0] = Node('if_statement', [t[3], t[6]])

def p_statement_3(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement %prec else_priority'
	t[0] = Node('if_statement', [t[3], t[5]])

def p_statement_4(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement ELSE statement'
	t[0] = Node('if_else_statement', [t[3], t[5], t[7]])

def p_statement_5(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL ELSE statement'
	t[0] = Node('if_else_statement', [t[3], t[6], t[9]])

def p_statement_6(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement ELSE LEFT_CURL statement_list RIGHT_CURL'
	t[0] = Node('if_else_statement', [t[3], t[5], t[8]])

def p_statement_7(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL ELSE LEFT_CURL statement_list RIGHT_CURL'
	t[0] = Node('if_else_statement', [t[3], t[6], t[10]])

def p_statement_8(t):
	'statement : FOR LEFT_ROUND expression_statement expression_statement expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL'
	t[0] = Node('for_statement', [t[3], t[4], t[5], t[8]])

def p_statement_9(t):
	'statement : FOR LEFT_ROUND expression_statement expression_statement expression RIGHT_ROUND statement'
	t[0] = Node('for_statement', [t[3], t[4], t[5], t[7]])

def p_statement_10(t):
	'statement : expression_statement'
	t[0] = t[1]

def p_expression_statement(t):
	'expression_statement : SEMICOLON'
	t[0] = Node(t[1],[])

def p_expression(t):
	'expression : SEMICOLON'
	t[0] = Node(t[1],[])

def p_array(t):
	'array : IDENTIFIER array_index'
	t[0]= Node('array',[Node(t[1], []), t[2]])

def p_array_index_1(t):
	'array_index : LEFT_SQUARE INT_NUM RIGHT_SQUARE array_index'
	t[0]= Node('array_index',[Node(t[2], []), t[4]])

def p_array_index_2(t):
	'array_index : LEFT_SQUARE INT_NUM RIGHT_SQUARE'
	t[0]=Node(t[2],[])

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

	ast = parser.parse(open(data).read(), debug=0)
	t = ast.makegraphicaltree()
	#t.write('graph.dot', format='raw', prog='dot')
	t.write_pdf('AST.pdf')

if __name__=='__main__':
	myParser()
