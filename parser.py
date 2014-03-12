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

def p_translation_unit_01(t):
    '''translation_unit : external_declaration'''
    t[0] = Node('TranslationUnit', [t[1]])

def p_translation_unit_02(t):
    '''translation_unit : translation_unit external_declaration'''
    t[0] = Node('TranslationUnit', [t[1],t[2]])

def p_external_declaration(t):
    '''external_declaration : function_definition
                            | declaration'''
    t[0] = Node('ExternalDeclaration', [t[1]])

def p_function_definition_01(t):
    '''function_definition : type_specifier declarator compound_statement'''
    t[0] = Node('FunctionDefn', [t[1], t[2], t[3]])

def p_function_definition_02(t):
    '''function_definition : STATIC type_specifier declarator compound_statement'''
    t[0] = Node('FunctionDefn', [Node(t[1],[]), t[2], t[3], t[4]])
    
def p_declaration_01(t):
    '''declaration : type_specifier declarator SEMICOLON'''
    t[0] = Node('Declaration', [t[1], t[2]])

def p_declaration_02(t):
    '''declaration : EXTERN type_specifier declarator SEMICOLON'''
    t[0] = Node('Declaration', [Node(t[1],[]), t[2], t[3]])

def p_declaration_list_opt_01(t):
    '''declaration_list_opt : empty'''
    t[0] = Node('Empty',[])

def p_declaration_list_opt_02(t):
    '''declaration_list_opt : declaration_list'''
    t[0] = Node('DeclarationListOpt', [t[1]])

def p_declaration_list_02(t):
    '''declaration_list : declaration'''
    t[0] = Node('DeclarationList', [t[1]])

def p_declaration_list_03(t):
    '''declaration_list : declaration_list declaration'''
    t[0] = Node('DeclarationList',[t[1], t[2]])
    
def p_type_specifier(t):
    '''type_specifier : INT
                      | CHAR'''
    t[0] = Node('TypeSpecifier', Node(t[1],[]))

def p_declarator_01(t):
    '''declarator : direct_declarator'''
    t[0] = Node('Declarator', [t[1]])

def p_declarator_02(t):
    '''declarator : MULTIPLY declarator'''
    t[0] = Node('Declarator', [Node(t[1], []), t[2]])

def p_direct_declarator_01(t):
    '''direct_declarator : IDENTIFIER'''
    t[0] = Node('DirectDeclaration', [Node(t[1],[])])

def p_direct_declarator_02(t):
    '''direct_declarator : direct_declarator LEFT_ROUND parameter_type_list RIGHT_ROUND'''
    t[0] = Node('DirectDeclaration', [t[1],t[3]])

def p_direct_declarator_03(t):
    '''direct_declarator : direct_declarator LEFT_ROUND RIGHT_ROUND'''
    t[0] = Node('DirectDeclaration', t[1])
    
def p_parameter_type_list_01(t):
    '''parameter_type_list : parameter_list'''
    t[0] = Node('ParameterTypeList', [t[1]])

def p_parameter_type_list_02(t):
    '''parameter_type_list : parameter_list COMMA ELLIPSIS'''
    t[0] = Node('ParameterTypeList', [t[1], Node(t[3],[])])

def p_parameter_list_01(t):
    '''parameter_list : parameter_declaration'''
    t[0] = Node('ParameterList', [t[1]])

def p_parameter_list_02(t):
    '''parameter_list : parameter_list COMMA parameter_declaration'''
    t[0] = Node('ParameterList', [t[1], t[3]])

def p_parameter_declaration(t):
    '''parameter_declaration : type_specifier declarator'''
    # NOTE: this is the same code as p_declaration_01!
    p_declaration_01(t)

def p_compound_statement_01(t):
    '''compound_statement : LEFT_CURL declaration_list_opt statement_list RIGHT_CURL'''
    t[0] = Node('CompoundStatement', [t[2], t[3]])

def p_compound_statement_02(t):
    '''compound_statement : LEFT_CURL declaration_list_opt RIGHT_CURL'''
    t[0] = Node('CompoundStatement',[t[2]])

def p_expression_statement(t):
    '''expression_statement : expression SEMICOLON'''
    t[0] = Node('ExpressionStatement',[t[1]])

def p_expression_01(t):
    '''expression : equality_expression'''
    t[0] = Node('Expression',[t[1]])

def p_expression_02(t):    
    '''expression : equality_expression EQUAL expression
                  | equality_expression ADD_ASSIGN expression
                  | equality_expression SUB_ASSIGN expression'''
    t[0] = Node('Expression', [t[1], Node(t[2],[]), t[3]])

def p_equality_expression_01(t):
    '''equality_expression : relational_expression'''
    t[0] = Node('EqualityExpression',t[1])

def p_equality_expression_02(t):    
    '''equality_expression : equality_expression EQ_OP relational_expression
                           | equality_expression NE_OP relational_expression'''
    t[0] = Node('EqualityExpression', [t[1], Node(t[2],[]), t[3]])

def p_relational_expression_01(t):
    '''relational_expression : additive_expression'''
    t[0] = Node('RelationalExpression', [t[1]])

def p_relational_expression_02(t):
    '''relational_expression : relational_expression L_OP additive_expression
                             | relational_expression G_OP additive_expression
                             | relational_expression LE_OP additive_expression
                             | relational_expression GE_OP additive_expression'''
    t[0] = Node('RelationalExpression', [t[1], Node(t[2],[]), t[3]])

def p_postfix_expression_01(t):
    '''postfix_expression : primary_expression'''
    t[0] = Node('postfix',[t[1]])

def p_postfix_expression_02(t):
    '''postfix_expression : postfix_expression LEFT_ROUND argument_expression_list RIGHT_ROUND'''
    t[0] = Node('postfix',[t[1], t[3]])

def p_postfix_expression_03(t):
    '''postfix_expression : postfix_expression LEFT_ROUND RIGHT_ROUND'''
    t[0] = Node('postfix',[t[1]])

def p_postfix_expression_04(t):
    '''postfix_expression : postfix_expression LEFT_SQUARE expression RIGHT_SQUARE'''
    t[0] = Node('postfix',[t[1], t[3]])

def p_argument_expression_list_01(t):
    '''argument_expression_list : expression'''
    t[0] = Node('argumentlist',[t[1]])

def p_argument_expression_list_02(t):
    '''argument_expression_list : argument_expression_list COMMA expression'''
    t[0] = Node('argumentlist',[t[1],t[3]])

def p_unary_expression_01(t):
    '''unary_expression : postfix_expression'''
    t[0] = Node('unary_exp',[t[1]])

def p_unary_expression_02(t):
    '''unary_expression : MINUS unary_expression'''
    t[0] = Node('minus_unary',[t[2]])

def p_unary_expression_03(t):
    '''unary_expression : PLUS unary_expression'''
    t[0] = Node('plus_unary',[t[2]])

def p_unary_expression_06(t):
    '''unary_expression : EXCLAMATION unary_expression'''
    # horrible hack for the '!' operator... Just insert an
    # (expr == 0) into the AST.
    t[0] = Node('unary_exclamation',[t[2]])

def p_unary_expression_04(t):
    '''unary_expression : MULTIPLY unary_expression'''
    t[0] = Node('unary_asterisk',[t[2]])

def p_unary_expression_05(t):
    '''unary_expression : AMPERSAND unary_expression'''
    t[0] = Node('ampersand',[t[2]])

def p_mult_expression_01(t):
    '''mult_expression : unary_expression'''
    t[0] = Node('multexp',[t[1]])

def p_mult_expression_02(t):
    '''mult_expression : mult_expression MULTIPLY unary_expression
                       | mult_expression DIVIDE unary_expression    
                       | mult_expression MODULO unary_expression'''
    t[0] = Node('multexp',[t[1], t[3], Node(t[2],[])])

def p_additive_expression_01(t):
    '''additive_expression : mult_expression'''
    t[0] = Node('additiveexp',[t[1]])

def p_additive_expression_02(t):
    '''additive_expression : additive_expression PLUS mult_expression
                           | additive_expression MINUS mult_expression'''
    t[0] = Node('additive',[t[1], t[3], Node(t[2],[])])

def p_primary_expression_01(t):
    '''primary_expression : IDENTIFIER'''
    t[0] = Node('primary',[t[1]])

def p_primary_expression_02(t):
    '''primary_expression : INT_NUM'''
    t[0] = Node('primary',Node(t[1],[]))

def p_primary_expression_03(t):
    '''primary_expression : REAL_NUM'''
    t[0] = Node('primary',Node(t[1],[]))

def p_primary_expression_04(t):
    '''primary_expression : CHARACTER'''
    t[0] = Node('primary',Node(t[1],[]))

def p_primary_expression_05(t):
    '''primary_expression : string_literal'''
    t[0] = Node('primary',[t[1]])

def p_primary_expression_06(t):
    '''primary_expression : LEFT_ROUND expression RIGHT_ROUND '''
    t[0] = Node('primary',[t[2]])

def p_string_literal_01(t):
    '''string_literal : STRING'''
    t[0] = Node('strliteral',Node(t[1],[]))

def p_string_literal_02(t):
	'''string_literal : string_literal STRING'''
	t[0] = Node('strliteral',[t[1],Node(t[2],[])])

def p_statement(t):
    '''statement : compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement'''
    t[0] = Node('stmnt',[t[1]])

def p_jump_statement_01(t):
    '''jump_statement : RETURN SEMICOLON'''
    t[0] = Node('return',[])
    
def p_jump_statement_02(t):
    '''jump_statement : RETURN expression SEMICOLON'''
    t[0] = Node('return_val',[])

def p_jump_statement_03(t):
    '''jump_statement : BREAK SEMICOLON'''
    t[0] = Node('break',[])

def p_jump_statement_04(t):
    '''jump_statement : CONTINUE SEMICOLON'''
    t[0] = Node('continue',[])

def p_iteration_statement_01(t):
    '''iteration_statement : WHILE LEFT_ROUND expression RIGHT_ROUND statement'''
    t[0] = Node('while',[t[3],t[5]])

def p_iteration_statement_02(t):
    '''iteration_statement : FOR LEFT_ROUND expression_statement expression_statement expression RIGHT_ROUND statement'''
    t[0] = Node('for',[t[3],t[4],t[5],t[7]])

def p_selection_statement_01(t):
    '''selection_statement : IF LEFT_ROUND expression RIGHT_ROUND statement'''
    t[0] = Node('if-then',[t[3],t[5]])

def p_selection_statement_02(t):
    '''selection_statement : IF LEFT_ROUND expression RIGHT_ROUND statement ELSE statement'''
    t[0] = Node('if-then-else',[t[3],t[5],t[7]])

def p_statement_list_02(t):
    '''statement_list : statement'''
    t[0] = Node('stmt-list',[t[1]])

def p_statement_list_03(t):
    '''statement_list : statement_list statement'''
    t[0] = Node('stmt-list',[t[1],t[2]])

def p_empty(t):
    'empty :'
    t[0] = Node('empty',[])


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