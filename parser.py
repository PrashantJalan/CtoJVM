import sys
from lexer import tokens
import ply.yacc as yacc
import pydot
import os

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

#Defining precedence
precedence = (
	('nonassoc', 'else_priority'),
	('nonassoc', 'ELSE'),
	('right', 'EQUAL', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN'),
	('left', 'OR_OP'),
	('left', 'AND_OP'),
	('left', 'EQ_OP', 'NE_OP'),
	('left', 'G_OP', 'GE_OP', 'LE_OP', 'L_OP'),
	('left', 'PLUS', 'MINUS'),
	('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
	('left', 'INC_OP', 'DEC_OP'),
)

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

def p_statement_1(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL %prec else_priority'
	t[0] = Node('if_statement', [t[3], t[6]])

def p_statement_2(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement %prec else_priority'
	t[0] = Node('if_statement', [t[3], Node('statement_list', [t[5]])])

def p_statement_3(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement ELSE statement'
	t[0] = Node('if_else_statement', [t[3], Node('statement_list', [t[5]]), Node('statement_list', [t[7]])])

def p_statement_4(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL ELSE statement'
	t[0] = Node('if_else_statement', [t[3], t[6], Node('statement_list', [t[9]])])

def p_statement_5(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement ELSE LEFT_CURL statement_list RIGHT_CURL'
	t[0] = Node('if_else_statement', [t[3], Node('statement_list', [t[5]]), t[8]])

def p_statement_6(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL ELSE LEFT_CURL statement_list RIGHT_CURL'
	t[0] = Node('if_else_statement', [t[3], t[6], t[10]])

def p_statement_7(t):
	'statement : FOR LEFT_ROUND expression_statement expression_statement expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL'
	t[0] = Node('for_statement', [t[3], t[4], t[5], t[8]])

def p_statement_8(t):
	'statement : FOR LEFT_ROUND expression_statement expression_statement expression RIGHT_ROUND statement'
	t[0] = Node('for_statement', [t[3], t[4], t[5], Node('statement_list', [t[7]])])

def p_statement_9(t):
	'statement : expression_statement'
	t[0] = t[1]

def p_statement_10(t):
	'statement : WHILE LEFT_ROUND expression RIGHT_ROUND LEFT_CURL statement_list RIGHT_CURL'
	t[0]=Node('while_statement', [t[3], t[6]])

def p_statement_11(t):
	'statement : WHILE LEFT_ROUND expression RIGHT_ROUND statement'
	t[0]=Node('while_statement', [t[3], Node('statement_list', [t[5]])])

def p_statement_12(t):
	'''statement : CONTINUE SEMICOLON
					| BREAK SEMICOLON
					| RETURN SEMICOLON'''
	t[0] = Node(t[1], [])

def p_statement_13(t):
	'statement : RETURN expression SEMICOLON'
	t[0] = Node('return_expression', [t[2]])
 
def p_statement_14(t):
	'statement : type_specifier declaration_list SEMICOLON'
	t[0] = Node('Declaration', [t[1], t[2]])

def p_declaration_list_1(t):
	'declaration_list : declaration'
	t[0] = Node('declaration_list', [t[1]])

def p_declaration_list_2(t):
	'declaration_list : declaration_list COMMA declaration'
	t[1].add(t[3])
	t[0] = t[1]

def p_declaration_1(t):
	'declaration : IDENTIFIER'
	t[0] = Node(t[1], [])

def p_declaration_2(t):
	'''declaration : array
					| equal_or_initialise'''
	t[0] = t[1]

def p_constant_1(t):
	'''constant : HEX_NUM
				| REAL_NUM
				| INT_NUM
				| CHARACTER
				| STRING
				| EXP_NUM'''
	t[0] = Node(t[1], [])

def p_constant_2(t):
	'''constant : PLUS HEX_NUM
				| PLUS REAL_NUM
				| PLUS INT_NUM
				| PLUS EXP_NUM'''
	t[0] = Node(t[2], [])

def p_constant_3(t):
	'''constant : MINUS HEX_NUM
				| MINUS REAL_NUM
				| MINUS INT_NUM
				| MINUS EXP_NUM'''
	t[2] = '-'+t[2]
	t[0] = Node(t[2], [])

def p_array(t):
	'array : IDENTIFIER array_index'
	t[0]= Node('array',[Node(t[1], []), t[2]])

def p_array_index_1(t):
	'array_index : array_index LEFT_SQUARE INT_NUM RIGHT_SQUARE'
	t[1].add(Node(t[3],[]))
	t[0] = t[1]

def p_array_index_2(t):
	'array_index : LEFT_SQUARE INT_NUM RIGHT_SQUARE'
	t[0] = Node('array_index', [Node(t[2],[])])

def p_expression_statement_1(t):
	'expression_statement : SEMICOLON'
	t[0] = Node(t[1],[])

def p_expression_statement_2(t):
	'expression_statement : expression SEMICOLON'
	t[0] = t[1]

def p_expression_1(t):
	'expression : expression PLUS expression'
	t[0]=Node('PLUS', [t[1], t[3]])

def p_expression_2(t):
	'expression : expression MINUS expression'
	t[0]=Node('MINUS', [t[1], t[3]])

def p_expression_3(t):
	'expression : expression MULTIPLY expression'
	t[0]=Node('MULTIPLY', [t[1], t[3]])

def p_expression_4(t):
	'expression : expression DIVIDE expression'
	t[0]=Node('DIVIDE', [t[1], t[3]])

def p_expression_5(t):
	'expression : expression L_OP expression'
	t[0]=Node('L_OP', [t[1], t[3]])

def p_expression_6(t):
	'expression : expression G_OP expression'
	t[0]=Node('G_OP', [t[1], t[3]])

def p_expression_7(t):
	'expression : expression NE_OP expression'
	t[0]=Node('NE_OP', [t[1], t[3]])

def p_expression_8(t):
	'expression : expression EQ_OP expression'
	t[0]=Node('EQ_OP', [t[1], t[3]])

def p_expression_9(t):
	'expression : expression GE_OP expression'
	t[0]=Node('GE_OP', [t[1], t[3]])

def p_expression_10(t):
	'expression : expression LE_OP expression'
	t[0]=Node('LE_OP', [t[1], t[3]])

def p_expression_11(t):
	'expression : expression AND_OP expression'
	t[0]=Node('AND_OP', [t[1], t[3]])

def p_expression_12(t):
	'expression : expression OR_OP expression'
	t[0]=Node('OR_OP', [t[1], t[3]])

def p_expression_13(t):
	'expression : LEFT_ROUND expression RIGHT_ROUND'
	t[0]=t[1]

def p_expression_14(t):
	'expression : IDENTIFIER'
	t[0] = Node(t[1], [])

def p_expression_15(t):
	'''expression : array
				  | constant '''
	t[0] = t[1]

def p_expression_16(t):
	'''expression : assignment
				  | unary_expression
				  | function_call'''
	t[0] = t[1]

def p_assignment_1(t):
	'assignment : equal_or_initialise'
	t[0] = t[1]

def p_equal_or_initialise(t):
	'equal_or_initialise : IDENTIFIER EQUAL expression'
	t[0] = Node('EQUAL', [Node(t[1], []), t[3]])

def p_assignment_2(t):
	'assignment : array EQUAL expression'
	t[0] = Node('EQUAL', [t[1], t[3]])
	
def p_assignment_3(t):
	'assignment : IDENTIFIER ADD_ASSIGN expression'
	t[0] = Node('ADD_ASSIGN', [Node(t[1], []), t[3]])

def p_assignment_4(t):
	'assignment : IDENTIFIER SUB_ASSIGN expression'
	t[0] = Node('SUB_ASSIGN', [Node(t[1], []), t[3]])

def p_assignment_5(t):
	'assignment : IDENTIFIER DIV_ASSIGN expression'
	t[0] = Node('DIV_ASSIGN', [Node(t[1], []), t[3]])

def p_assignment_6(t):
	'assignment : IDENTIFIER MUL_ASSIGN expression'
	t[0] = Node('MUL_ASSIGN', [Node(t[1], []), t[3]])

def p_assignment_7(t):
	'assignment : IDENTIFIER MOD_ASSIGN expression'
	t[0] = Node('MOD_ASSIGN', [Node(t[1], []), t[3]])

def p_assignment_8(t):
	'assignment : array ADD_ASSIGN expression'
	t[0] = Node('ADD_ASSIGN', [t[1], t[3]])

def p_assignment_9(t):
	'assignment : array SUB_ASSIGN expression'
	t[0] = Node('SUB_ASSIGN', [t[1], t[3]])

def p_assignment_10(t):
	'assignment : array DIV_ASSIGN expression'
	t[0] = Node('DIV_ASSIGN', [t[1], t[3]])

def p_assignment_11(t):
	'assignment : array MUL_ASSIGN expression'
	t[0] = Node('MUL_ASSIGN', [t[1], t[3]])

def p_assignment_11(t):
	'assignment : array MOD_ASSIGN expression'
	t[0] = Node('MOD_ASSIGN', [t[1], t[3]])

def p_unary_expression_1(t):
	'unary_expression : IDENTIFIER INC_OP'
	t[0]= Node('post_increment', [Node(t[1],[])])

def p_unary_expression_2(t):
	'unary_expression : IDENTIFIER DEC_OP'
	t[0]= Node('post_decrement', [Node(t[1],[])])

def p_unary_expression_3(t):
	'unary_expression : array INC_OP'
	t[0]= Node('post_increment', [t[1]])

def p_unary_expression_4(t):
	'unary_expression : array DEC_OP'
	t[0]= Node('post_decrement', [t[1]])

def p_unary_expression_5(t):
	'unary_expression : INC_OP IDENTIFIER'
	t[0]= Node('pre_increment', [Node(t[2],[])])

def p_unary_expression_6(t):
	'unary_expression : INC_OP array'
	t[0]= Node('pre_increment', [t[2]])

def p_unary_expression_7(t):
	'unary_expression : DEC_OP IDENTIFIER'
	t[0]= Node('pre_decrement', [Node(t[2],[])])

def p_unary_expression_8(t):
	'unary_expression : DEC_OP array'
	t[0]= Node('pre_decrement', [t[2]])

def p_function_call(t):
	'function_call : IDENTIFIER LEFT_ROUND function_call_list RIGHT_ROUND'
	t[0] = Node('function_call',[Node(t[1],[]), t[3]])

def p_function_call_list_1(t):
	'function_call_list : function_argument'
	t[0] = Node('function_call_list',[t[1]])

def p_function_call_list_2(t):
	'function_call_list : function_call_list COMMA function_argument'
	t[1].add(t[3])
	t[0] = t[1]

def p_function_argument_1(t):
	'function_argument : IDENTIFIER'
	t[0]= Node(t[1], [])

def p_function_argument_2(t):
	'''function_argument : array
				| constant'''
	t[0] = t[1]

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
