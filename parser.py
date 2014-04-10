#problem with post increment
import sys
from lexer import tokens
import ply.yacc as yacc
import pydot
import os

def checkIdentifierError(t):
	res = currentSymbolTable.get(t)
	if res==None:
		sys.stdout.write("Error! "+t+" not declared.\n")
	else:
		if res[1].type=="argument_list":
			sys.stdout.write("Error! "+t+" declared as a function.\n")

def checkFunctionError(t):
	res = currentSymbolTable.get(t.children[0].type)
	if res==None:
		sys.stdout.write("Error! "+t.children[0].type+" function not declared.\n")
	else:
		if res[1].type!="argument_list":
			sys.stdout.write("Error! "+t.children[0].type+" not declared as a function.\n")
		else:
			if len(res[1].children)!=len(t.children[1].children):
				sys.stdout.write("Error! Function argument length mismatch for "+t.children[0].type+".\n")

def checkArrayError(t):
	res = currentSymbolTable.get(t.children[0].type)
	if res==None:
		sys.stdout.write("Error! Array "+t.children[0].type+" not declared.\n")
	else:
		if res[1].type=="argument_list":
			sys.stdout.write("Error! "+t+" declared as a function.\n")
		elif len(res[1].children)!=len(t.children[1].children):
			sys.stdout.write("Error! Array index length mismatch for "+t.children[0].type+".\n")

#Symbol Table
SymbolTableCount = 0
class SymbolTable:
    """A symbol table class. There is a separate symbol table for 
    each code element that has its own scope."""

    def __init__(self, parent=None):
    	global SymbolTableCount
        self.entries = {}
        self.ID = str(SymbolTableCount)
        SymbolTableCount += 1
        self.parent = parent
        if self.parent != None:
            self.parent.children.append(self)
        self.children = []
    
    def makegraphicaltree2(self, dot=None):
    	global SymbolTableCount
    	if not dot: dot = pydot.Dot()
    	dot.add_node(pydot.Node(self.ID, label='table', shape='ellipse'))
    	for c in self.children:
    		c.makegraphicaltree2(dot)
    		edge = pydot.Edge(self.ID,c.ID)
    		dot.add_edge(edge)
    	entryID = SymbolTableCount
    	dot.add_node(pydot.Node(entryID, label='entries', shape='ellipse'))
    	edge = pydot.Edge(self.ID,entryID)
    	dot.add_edge(edge)
    	SymbolTableCount += 1
    	for item in self.entries:
    		temp = SymbolTableCount
    		dot.add_node(pydot.Node(temp, label=item, shape='ellipse'))
    		edge = pydot.Edge(entryID,temp)
    		dot.add_edge(edge)
    		SymbolTableCount += 1
    		temp2 = SymbolTableCount
    		dot.add_node(pydot.Node(temp2, label=self.entries[item][0], shape='ellipse'))
    		edge = pydot.Edge(temp,temp2)
    		dot.add_edge(edge)
    		SymbolTableCount += 1
    		if self.entries[item][1].type:
    			temp3 = SymbolTableCount
    			dot.add_node(pydot.Node(temp3, label=self.entries[item][1].type, shape='ellipse'))
    			edge = pydot.Edge(temp,temp3)
    			dot.add_edge(edge)
    			SymbolTableCount += 1
    	return dot


    def add(self, name, type, attribute=None):
    	if self.get(name)!=None:
            sys.stdout.write("Error! Variable "+name+" redefined.\n")
        else:
        	if attribute==None:
        		self.entries[name] = [type, Node('',[])]
        	else:
        		self.entries[name] = [type, attribute]

    def get(self, name):
        if self.entries.has_key(name):
            return self.entries[name]
        else:
            if self.parent != None:
                return self.parent.get(name)
            else:
                return None

	

#Tree Node for AST
class Node:
	labelCount=0
	varCount=0
	count  = 0
	type = 'Node(unspecified)'
	shape = 'ellipse'
	def __init__(self, type, children=None):
		self.ID = str(Node.count)
		self.parent = None
		self.type = type
		self.code=[]
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

	def addCode(self, c):
		#print c
		if c!=[]:
			self.code = self.code + c
			#print self.type,self.code

	def newLabel(self):
		Node.labelCount=Node.labelCount+1
		return "label"+str(Node.labelCount)

	def newVar(self):
		Node.varCount=Node.varCount+1
		self.var="var"+str(Node.varCount)
		return self.var

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
currentSymbolTable = SymbolTable()

def p_program(t):
	'program : function_list'
	t[0] = t[1]

def p_function_list_1(t):
	'function_list : function_list function'
	t[1].add(t[2])
	t[0] = t[1]
	t[0].addCode(t[2].code)

def p_function_list_2(t):
	'function_list : function'
	t[0] = Node('function_list', [t[1]])
	t[0].addCode(t[1].code)

def p_function_1(t):
	'function : function_definition'
	t[0]=t[1]

def p_function_2(t):
	'function : declaration_statement'
	t[0]=t[1]

def p_type_specifier(t):
	'''type_specifier : CHAR
						| VOID
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
	currentSymbolTable.add(t[2], t[1].type)
	
def p_argument_2(t):
	'argument : type_specifier array'
	t[0]= Node('argument',[t[1], t[2]])
	currentSymbolTable.add(t[2].children[0].type, t[1].type, t[2].children[1])

def p_function_definition_1(t):
	'function_definition : type_specifier IDENTIFIER LEFT_ROUND argument_list RIGHT_ROUND left_curl statement_list right_curl'
	t[0] = Node('function_definition', [t[1], Node(t[2], []), t[4], t[7]])
	currentSymbolTable.add(t[2], t[1].type, t[4])
	nLabel = t[2]+":"
	t[0].addCode([nLabel])
	t[0].addCode(t[7].code)

def p_function_definition_2(t):
	'function_definition : type_specifier IDENTIFIER LEFT_ROUND RIGHT_ROUND left_curl statement_list right_curl'
	t[0] = Node('function_definition', [t[1], Node(t[2], []), Node('argument_list', []), t[6]])
	currentSymbolTable.add(t[2], t[1].type, Node('argument_list', []))
	nLabel = t[2]+":"
	t[0].addCode([nLabel])
	t[0].addCode(t[6].code)

def p_statement_list_1(t):
	'statement_list : statement_list statement'
	t[1].add(t[2])
	t[0] = t[1]
	t[0].addCode(t[2].code)

def p_statement_list_2(t):
	'statement_list : statement'
	t[0] = Node('statement_list', [t[1]])
	t[0].addCode(t[1].code)

def p_statement_1(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND left_curl statement_list right_curl %prec else_priority'
	t[0] = Node('if_statement', [t[3], t[6]])
	Ef = t[3].newLabel()
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[3].var+"==0 goto "+Ef])
	t[0].addCode(t[6].code)
	t[0].addCode([Ef+":"])

def p_statement_2(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement %prec else_priority'
	t[0] = Node('if_statement', [t[3], Node('statement_list', [t[5]])])
	Ef = t[3].newLabel()
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[3].var+"==0 goto "+Ef])
	t[0].addCode(t[5].code)
	t[0].addCode([Ef+":"])	

def p_statement_3(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement ELSE statement'
	t[0] = Node('if_else_statement', [t[3], Node('statement_list', [t[5]]), Node('statement_list', [t[7]])])
	Ef = t[3].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[3].var+"==0 goto "+Ef])
	t[0].addCode(t[5].code)
	gen = "goto "+Sn
	t[0].addCode([gen])
	gen = Ef+":"
	t[0].addCode([gen])
	t[0].addCode(t[7].code)
	t[0].addCode([Sn+":"])

def p_statement_4(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND left_curl statement_list right_curl ELSE statement'
	t[0] = Node('if_else_statement', [t[3], t[6], Node('statement_list', [t[9]])])
	Ef = t[3].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[3].var+"==0 goto "+Ef])
	t[0].addCode(t[6].code)
	gen = "goto "+Sn
	t[0].addCode([gen])
	gen = Ef+":"
	t[0].addCode([gen])
	t[0].addCode(t[9].code)
	t[0].addCode([Sn+":"])

def p_statement_5(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND statement ELSE left_curl statement_list right_curl'
	t[0] = Node('if_else_statement', [t[3], Node('statement_list', [t[5]]), t[8]])
	Ef = t[3].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[3].var+"==0 goto "+Ef])
	t[0].addCode(t[5].code)
	gen = "goto "+Sn
	t[0].addCode([gen])
	gen = Ef+":"
	t[0].addCode([gen])
	t[0].addCode(t[8].code)
	t[0].addCode([Sn+":"])

def p_statement_6(t):
	'statement : IF LEFT_ROUND expression RIGHT_ROUND left_curl statement_list right_curl ELSE left_curl statement_list right_curl'
	t[0] = Node('if_else_statement', [t[3], t[6], t[10]])
	Et = t[3].newLabel()
	Ef = t[3].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[3].var+"==0 goto "+Ef])
	t[0].addCode(t[6].code)
	gen = "goto "+Sn
	t[0].addCode([gen])
	gen = Ef+":"
	t[0].addCode([gen])
	t[0].addCode(t[10].code)
	t[0].addCode([Sn+":"])

def p_statement_7(t):
	'statement : FOR LEFT_ROUND expression_statement expression_statement expression RIGHT_ROUND left_curl statement_list right_curl'
	t[0] = Node('for_statement', [t[3], t[4], t[5], t[8]])
	Sb = t[0].newLabel()
	Sn = t[0].newLabel()
	Et = t[3].newLabel()
	Ef = Sn
	S1n = Sb
	t[0].addCode(t[3].code)
	t[0].addCode([Sb+":"])
	t[0].addCode(t[4].code)
	t[0].addCode(["if "+t[4].var+"==0 goto "+Ef])
	j = 0
	while j<len(t[8].code):
		if t[8].code[j]=="goto continue":
			t[8].code[j]="goto "+Sb
		elif t[8].code[j]=="goto break":
			t[8].code[j]="goto "+Ef
		j+=1
	t[0].addCode(t[8].code)
	t[0].addCode(t[5].code)
	t[0].addCode(["goto "+S1n])
	t[0].addCode([Ef+":"])


def p_statement_8(t):
	'statement : FOR LEFT_ROUND expression_statement expression_statement expression RIGHT_ROUND statement'
	t[0] = Node('for_statement', [t[3], t[4], t[5], Node('statement_list', [t[7]])])
	Sb = t[0].newLabel()
	Sn = t[0].newLabel()
	Et = t[3].newLabel()
	Ef = Sn
	S1n = Sb
	t[0].addCode(t[3].code)
	t[0].addCode([Sb+":"])
	t[0].addCode(t[4].code)
	t[0].addCode(["if "+t[4].var+"==0 goto "+Ef])
	j = 0
	while j<len(t[7].code):
		if t[7].code[j]=="goto continue":
			t[7].code[j]="goto "+Sb
		elif t[7].code[j]=="goto break":
			t[7].code[j]="goto "+Ef
		j+=1
	t[0].addCode(t[7].code)
	t[0].addCode(t[5].code)
	t[0].addCode(["goto "+S1n])
	t[0].addCode([Ef+":"])

def p_statement_9(t):
	'statement : expression_statement'
	t[0] = t[1]

def p_statement_10(t):
	'statement : WHILE LEFT_ROUND expression RIGHT_ROUND left_curl statement_list right_curl'
	t[0]=Node('while_statement', [t[3], t[6]])
	Sb = t[0].newLabel()
	Sn = t[0].newLabel()
	Et = t[3].newLabel()
	Ef = Sn
	S1n = Sb
	t[0].addCode([Sb+":"])
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[3].var+"==0 goto "+Ef])
	j = 0
	while j<len(t[6].code):
		if t[6].code[j]=="goto continue":
			t[6].code[j]="goto "+Sb
		elif t[6].code[j]=="goto break":
			t[6].code[j]="goto "+Ef
		j+=1
	t[0].addCode(t[6].code)
	t[0].addCode(["goto "+S1n])
	t[0].addCode([Ef+":"])

def p_statement_11(t):
	'statement : WHILE LEFT_ROUND expression RIGHT_ROUND statement'
	t[0]=Node('while_statement', [t[3], Node('statement_list', [t[5]])])
	Sb = t[0].newLabel()
	Sn = t[0].newLabel()
	Et = t[3].newLabel()
	Ef = Sn
	S1n = Sb
	t[0].addCode([Sb+":"])
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[3].var+"==0 goto "+Ef])
	j = 0
	while j<len(t[5].code):
		if t[5].code[j]=="goto continue":
			t[5].code[j]="goto "+Sb
		elif t[5].code[j]=="goto break":
			t[5].code[j]="goto "+Ef
		j+=1
	t[0].addCode(t[5].code)
	t[0].addCode(["goto "+S1n])
	t[0].addCode([Ef+":"])

def p_statement_12(t):
	'''statement : RETURN SEMICOLON'''
	t[0] = Node(t[1], [])

def p_statement_13(t):
	'statement : RETURN expression SEMICOLON'
	t[0] = Node('return_expression', [t[2]])
 
def p_statement_14(t):
	'statement : declaration_statement'
	t[0] = t[1]

def p_statement_15(t):
	'''statement : CONTINUE SEMICOLON'''
	t[0] = Node(t[1], [])
	t[0].addCode(["goto continue"])

def p_statement_16(t):
	'''statement : BREAK SEMICOLON'''
	t[0] = Node(t[1], [])
	t[0].addCode(["goto break"])

def p_declaration_statement(t):
	'declaration_statement : type_specifier declaration_list SEMICOLON'
	t[0] = Node('Declaration', [t[1], t[2]])
	for item in t[2].children:
		if len(item.children)==0:
			currentSymbolTable.add(item.type, t[1].type)
		else:
			if item.type=="array":
				currentSymbolTable.add(item.children[0].type, t[1].type, item.children[1])
			else:
				currentSymbolTable.add(item.children[0].type, t[1].type)
	t[0].addCode(t[2].code)

def p_declaration_list_1(t):
	'declaration_list : declaration'
	t[0] = Node('declaration_list', [t[1]])
	t[0].addCode(t[1].code)

def p_declaration_list_2(t):
	'declaration_list : declaration_list COMMA declaration'
	t[1].add(t[3])
	t[0] = t[1]
	t[0].addCode(t[3].code)

def p_declaration_1(t):
	'declaration : IDENTIFIER'
	t[0] = Node(t[1], [])

def p_declaration_2(t):
	'''declaration : array
					| declaration_assignment'''
	t[0] = t[1]

def p_declaration_assignment(t):
	'declaration_assignment : IDENTIFIER EQUAL expression'
	t[0] = Node('EQUAL', [Node(t[1], []), t[3]])
	t[0].addCode(t[3].code)
	gen = t[1]+"="+t[3].var
	t[0].addCode([gen])

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
	'array_index : array_index LEFT_SQUARE expression RIGHT_SQUARE'
	t[1].add(t[3])
	t[0] = t[1]

def p_array_index_2(t):
	'array_index : LEFT_SQUARE expression RIGHT_SQUARE'
	t[0] = Node('array_index', [t[2]])

def p_expression_statement_1(t):
	'expression_statement : SEMICOLON'
	t[0] = Node(t[1],[])

def p_expression_statement_2(t):
	'expression_statement : expression SEMICOLON'
	t[0] = t[1]

def p_expression_1(t):
	'expression : expression PLUS expression'
	t[0]=Node('PLUS', [t[1], t[3]])
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	nvar = t[0].newVar()
	gen = nvar+"="+t[1].var+"+"+t[3].var
	t[0].addCode([gen])

def p_expression_2(t):
	'expression : expression MINUS expression'
	t[0]=Node('MINUS', [t[1], t[3]])
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	nvar = t[0].newVar()
	gen = nvar+"="+t[1].var+"-"+t[3].var
	t[0].addCode([gen])

def p_expression_3(t):
	'expression : expression MULTIPLY expression'
	t[0]=Node('MULTIPLY', [t[1], t[3]])
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	nvar = t[0].newVar()
	gen = nvar+"="+t[1].var+"*"+t[3].var
	t[0].addCode([gen])

def p_expression_4(t):
	'expression : expression DIVIDE expression'
	t[0]=Node('DIVIDE', [t[1], t[3]])
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	nvar = t[0].newVar()
	gen = nvar+"="+t[1].var+"/"+t[3].var
	t[0].addCode([gen])

def p_expression_5(t):
	'expression : expression L_OP expression'
	t[0]=Node('L_OP', [t[1], t[3]])
	nvar = t[0].newVar()
	true = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[1].var+" < "+t[3].var+" goto "+true])
	t[0].addCode([nvar+"=0"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([true+":"])
	t[0].addCode([nvar+"=1"])
	t[0].addCode([Sn+":"])

def p_expression_6(t):
	'expression : expression G_OP expression'
	t[0]=Node('G_OP', [t[1], t[3]])
	nvar = t[0].newVar()
	nvar = t[0].newVar()
	true = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[1].var+" > "+t[3].var+" goto "+true])
	t[0].addCode([nvar+"=0"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([true+":"])
	t[0].addCode([nvar+"=1"])
	t[0].addCode([Sn+":"])

def p_expression_7(t):
	'expression : expression NE_OP expression'
	t[0]=Node('NE_OP', [t[1], t[3]])
	nvar = t[0].newVar()
	true = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[1].var+" != "+t[3].var+" goto "+true])
	t[0].addCode([nvar+"=0"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([true+":"])
	t[0].addCode([nvar+"=1"])
	t[0].addCode([Sn+":"])

def p_expression_8(t):
	'expression : expression EQ_OP expression'
	t[0]=Node('EQ_OP', [t[1], t[3]])
	nvar = t[0].newVar()
	true = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[1].var+" == "+t[3].var+" goto "+true])
	t[0].addCode([nvar+"=0"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([true+":"])
	t[0].addCode([nvar+"=1"])
	t[0].addCode([Sn+":"])

def p_expression_9(t):
	'expression : expression GE_OP expression'
	t[0]=Node('GE_OP', [t[1], t[3]])
	nvar = t[0].newVar()
	true = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[1].var+" >= "+t[3].var+" goto "+true])
	t[0].addCode([nvar+"=0"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([true+":"])
	t[0].addCode([nvar+"=1"])
	t[0].addCode([Sn+":"])

def p_expression_10(t):
	'expression : expression LE_OP expression'
	t[0]=Node('LE_OP', [t[1], t[3]])
	nvar = t[0].newVar()
	true = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[1].var+" <= "+t[3].var+" goto "+true])
	t[0].addCode([nvar+"=0"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([true+":"])
	t[0].addCode([nvar+"=1"])
	t[0].addCode([Sn+":"])

def p_expression_11(t):
	'expression : expression AND_OP expression'
	t[0]=Node('AND_OP', [t[1], t[3]])
	nvar = t[0].newVar()
	false = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(["if "+t[1].var+"==0 goto "+false])
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[1].var+"==0 goto "+false])
	t[0].addCode([nvar+"=1"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([false+":"])
	t[0].addCode([nvar+"=0"])
	t[0].addCode([Sn+":"])

def p_expression_12(t):
	'expression : expression OR_OP expression'
	t[0]=Node('OR_OP', [t[1], t[3]])
	nvar = t[0].newVar()
	true = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(["if "+t[1].var+"==1 goto "+true])
	t[0].addCode(t[3].code)
	t[0].addCode(["if "+t[1].var+"==1 goto "+true])
	t[0].addCode([nvar+"=0"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([true+":"])
	t[0].addCode([nvar+"=1"])
	t[0].addCode([Sn+":"])

def p_expression_13(t):
	'expression : LEFT_ROUND expression RIGHT_ROUND'
	t[0]=t[1]

def p_expression_14(t):
	'expression : IDENTIFIER'
	t[0] = Node(t[1], [])
	checkIdentifierError(t[1])
	nvar = t[0].newVar()
	gen = nvar+"="+t[1]
	t[0].addCode([gen])

def p_expression_15(t):
	'''expression : array'''
	t[0] = t[1]
	checkArrayError(t[1])
	nvar = t[0].newVar()
	gen = nvar+"="+str(t[1].type)
	t[0].addCode([gen])

def p_expression_16(t):
	'''expression : constant '''
	t[0] = t[1]
	nvar = t[0].newVar()
	gen = nvar+"="+str(t[1].type)
	t[0].addCode([gen])

def p_expression_17(t):
	'''expression : assignment
				  | unary_expression
				  | function_call'''
	t[0] = t[1]

def p_expression_18(t):
	'expression : TILDA expression'
	t[0] = Node('NOT', [t[1]])
	nvar = t[0].newVar()
	true = t[0].newLabel()
	Sn = t[0].newLabel()
	t[0].addCode(t[1].code)
	t[0].addCode(["if "+t[1].var+"==0 goto "+true])
	t[0].addCode([nvar+"=0"])
	t[0].addCode(["goto "+Sn])
	t[0].addCode([true+":"])
	t[0].addCode([nvar+"=1"])
	t[0].addCode([Sn+":"])

def p_assignment_1(t):
	'assignment : array EQUAL expression'
	t[0] = Node('EQUAL', [t[1], t[3]])
	checkArrayError(t[1])
	
def p_assignment_2(t):
	'assignment : IDENTIFIER EQUAL expression'
	t[0] = Node('EQUAL', [Node(t[1], []), t[3]])
	checkIdentifierError(t[1])
	t[0].addCode(t[3].code)
	gen = t[1]+"="+t[3].var
	t[0].addCode([gen])
	
def p_assignment_3(t):
	'assignment : IDENTIFIER ADD_ASSIGN expression'
	t[0] = Node('ADD_ASSIGN', [Node(t[1], []), t[3]])
	checkIdentifierError(t[1])
	t[0].addCode(t[3].code)
	gen = t[1]+"="+t[1]+" + "+t[3].var
	t[0].addCode([gen])

def p_assignment_4(t):
	'assignment : IDENTIFIER SUB_ASSIGN expression'
	t[0] = Node('SUB_ASSIGN', [Node(t[1], []), t[3]])
	checkIdentifierError(t[1])
	t[0].addCode(t[3].code)
	gen = t[1]+"="+t[1]+" - "+t[3].var
	t[0].addCode([gen])

def p_assignment_5(t):
	'assignment : IDENTIFIER DIV_ASSIGN expression'
	t[0] = Node('DIV_ASSIGN', [Node(t[1], []), t[3]])
	checkIdentifierError(t[1])
	t[0].addCode(t[3].code)
	gen = t[1]+"="+t[1]+" / "+t[3].var
	t[0].addCode([gen])

def p_assignment_6(t):
	'assignment : IDENTIFIER MUL_ASSIGN expression'
	t[0] = Node('MUL_ASSIGN', [Node(t[1], []), t[3]])
	checkIdentifierError(t[1])
	t[0].addCode(t[3].code)
	gen = t[1]+"="+t[1]+" * "+t[3].var
	t[0].addCode([gen])

def p_assignment_7(t):
	'assignment : IDENTIFIER MOD_ASSIGN expression'
	t[0] = Node('MOD_ASSIGN', [Node(t[1], []), t[3]])
	checkIdentifierError(t[1])
	t[0].addCode(t[3].code)
	gen = t[1]+"="+t[1]+" % "+t[3].var
	t[0].addCode([gen])

def p_assignment_8(t):
	'assignment : array ADD_ASSIGN expression'
	t[0] = Node('ADD_ASSIGN', [t[1], t[3]])
	checkArrayError(t[1])

def p_assignment_9(t):
	'assignment : array SUB_ASSIGN expression'
	t[0] = Node('SUB_ASSIGN', [t[1], t[3]])
	checkArrayError(t[1])

def p_assignment_10(t):
	'assignment : array DIV_ASSIGN expression'
	t[0] = Node('DIV_ASSIGN', [t[1], t[3]])
	checkArrayError(t[1])

def p_assignment_11(t):
	'assignment : array MUL_ASSIGN expression'
	t[0] = Node('MUL_ASSIGN', [t[1], t[3]])
	checkArrayError(t[1])

def p_assignment_12(t):
	'assignment : array MOD_ASSIGN expression'
	t[0] = Node('MOD_ASSIGN', [t[1], t[3]])
	checkArrayError(t[1])

def p_unary_expression_1(t):
	'unary_expression : IDENTIFIER INC_OP'
	t[0]= Node('post_increment', [Node(t[1],[])])
	checkIdentifierError(t[1])
	nvar = t[0].newVar()
	t[0].addCode([nvar+"="+t[1]])
	t[0].addCode([t[1]+"="+t[1]+"+1"])

def p_unary_expression_2(t):
	'unary_expression : IDENTIFIER DEC_OP'
	t[0]= Node('post_decrement', [Node(t[1],[])])
	checkIdentifierError(t[1])
	nvar = t[0].newVar()
	t[0].addCode([nvar+"="+t[1]])
	t[0].addCode([t[1]+"="+t[1]+"-1"])

def p_unary_expression_3(t):
	'unary_expression : array INC_OP'
	t[0]= Node('post_increment', [t[1]])
	checkArrayError(t[1])

def p_unary_expression_4(t):
	'unary_expression : array DEC_OP'
	t[0]= Node('post_decrement', [t[1]])
	checkArrayError(t[1])

def p_unary_expression_5(t):
	'unary_expression : INC_OP IDENTIFIER'
	t[0]= Node('pre_increment', [Node(t[2],[])])
	checkIdentifierError(t[2])
	nvar = t[0].newVar()
	t[0].addCode([nvar+"="+t[2]+"+1"])
	t[0].addCode([t[2]+"="+nvar])

def p_unary_expression_6(t):
	'unary_expression : INC_OP array'
	t[0]= Node('pre_increment', [t[2]])
	checkArrayError(t[2])

def p_unary_expression_7(t):
	'unary_expression : DEC_OP IDENTIFIER'
	t[0]= Node('pre_decrement', [Node(t[2],[])])
	checkIdentifierError(t[2])
	nvar = t[0].newVar()
	t[0].addCode([nvar+"="+t[2]+"-1"])
	t[0].addCode([t[2]+"="+nvar])

def p_unary_expression_8(t):
	'unary_expression : DEC_OP array'
	t[0]= Node('pre_decrement', [t[2]])
	checkArrayError(t[2])

def p_function_call_1(t):
	'function_call : IDENTIFIER LEFT_ROUND function_call_list RIGHT_ROUND'
	t[0] = Node('function_call',[Node(t[1],[]), t[3]])
	checkFunctionError(t[0])

def p_function_call_2(t):
	'function_call : IDENTIFIER LEFT_ROUND RIGHT_ROUND'
	t[0] = Node('function_call',[Node(t[1],[]), Node('function_call_list', [])])
	checkFunctionError(t[0])

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
	checkIdentifierError(t[1])

def p_function_argument_2(t):
	'''function_argument : array'''
	t[0] = t[1]
	checkArrayError(t[1])

def p_function_argument_3(t):
	'''function_argument : constant'''
	t[0] = t[1]

def p_left_curl(t):
	'left_curl :  LEFT_CURL'
	global currentSymbolTable
	currentSymbolTable = SymbolTable(currentSymbolTable)

def p_right_curl(t):
	'right_curl :  RIGHT_CURL'
	global currentSymbolTable
	currentSymbolTable = currentSymbolTable.parent

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
	s = currentSymbolTable.makegraphicaltree2()
	#t.write('graph.dot', format='raw', prog='dot')
	t.write_pdf('AST.pdf')
	s.write_pdf('SymbolTable.pdf')
	mir = open("3AddressCode.txt",'w')
	for c in ast.code:
		if c=="goto continue" or c=="goto break":
			print "ERROR! break or continue not in loop."
		mir.write(c+'\n')
	mir.close()

if __name__=='__main__':
	myParser()
