import sys
from lexer import tokens
import ply.yacc as yacc
import pydot
import os

#Printing AST; Debugging purpose

precedence = (
	('nonassoc','else_priority'), 
	('nonassoc','ELSE'),
)

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

start = 'translation_unit'

#Grammar definitions
def p_primary_expression_1(t):
	'primary_expression : IDENTIFIER'
	t[0]=Node(t[1], [])
def p_primary_expression_2(t):
	'primary_expression : STRING'
	t[0]=Node(t[1], [])
def p_primary_expression_3(t):
	'primary_expression : INT_NUM'
	t[0]=Node(t[1], [])
def p_primary_expression_4(t):
	'primary_expression : HEX_NUM'
	t[0]=Node(t[1], [])
def p_primary_expression_5(t):
	'primary_expression : EXP_NUM'
	t[0]=Node(t[1], [])
def p_primary_expression_6(t):
	'primary_expression : REAL_NUM'
	t[0]=Node(t[1], [])
def p_primary_expression_7(t):
	'primary_expression : CHARACTER'
	t[0]=Node(t[1], [])
def p_primary_expression_8(t):
	'primary_expression : LEFT_ROUND expression RIGHT_ROUND'
	t[0]=t[2]	
def p_postfix_expression_1(t):
	'postfix_expression : primary_expression'
	t[0]=t[1]
def p_postfix_expression_2(t):
	'postfix_expression : postfix_expression LEFT_SQUARE expression RIGHT_SQUARE'
	t[0]=Node('postfix_expression', [t[1], t[3]])
def p_postfix_expression_3(t):
	'postfix_expression : postfix_expression LEFT_ROUND RIGHT_ROUND'
	t[0]=Node('postfix_expression', [t[1],Node('argument_expression_list',[])])
def p_postfix_expression_4(t):
	'postfix_expression : postfix_expression LEFT_ROUND argument_expression_list RIGHT_ROUND'
	t[0]=Node('postfix_expression', [t[1],t[3]])
def p_postfix_expression_5(t):
	'postfix_expression : postfix_expression DOT IDENTIFIER'
	t[0]=Node('postfix_expression', [t[1],Node(t[2], []),Node(t[3], [])])
def p_postfix_expression_6(t):
	'postfix_expression : postfix_expression PTR_OP IDENTIFIER'
	t[0]=Node('postfix_expression', [t[1],Node(t[2], []),Node(t[3], [])])
def p_postfix_expression_7(t):
	'postfix_expression : postfix_expression INC_OP'
	t[0]=Node('postfix_expression', [t[1],Node(t[2], [])])
def p_postfix_expression_8(t):
	'postfix_expression : postfix_expression DEC_OP'
	t[0]=Node('postfix_expression', [t[1],Node(t[2], [])])
def p_argument_expression_list_1(t):
	'argument_expression_list : assignment_expression'
	t[0]=t[1]
def p_argument_expression_list_2(t):
	'argument_expression_list : argument_expression_list COMMA assignment_expression'
	t[0]=Node('argument_expression_list', [t[1],t[3]])
def p_unary_expression_1(t):
	'unary_expression : postfix_expression'
	t[0]=t[1]
def p_unary_expression_2(t):
	'unary_expression : INC_OP unary_expression'
	t[0]=Node('unary_expression', [Node(t[1], []),t[2]])
def p_unary_expression_3(t):
	'unary_expression : DEC_OP unary_expression'
	t[0]=Node('unary_expression', [Node(t[1], []),t[2]])
def p_unary_expression_4(t):
	'unary_expression : unary_operator cast_expression'
	t[0]=Node('unary_expression', [t[1],t[2]])
def p_unary_expression_5(t):
	'unary_expression : SIZEOF unary_expression'
	t[0]=Node('unary_expression', [Node(t[1], []),t[2]])
def p_unary_expression_6(t):
	'unary_expression : SIZEOF LEFT_ROUND type_name RIGHT_ROUND'
	t[0]=Node('unary_expression', [Node(t[1], []),t[3]])
def p_unary_operator_1(t):
	'unary_operator : AMPERSAND'
	t[0]=Node(t[1], [])
def p_unary_operator_2(t):
	'unary_operator : MULTIPLY'
	t[0]=Node(t[1], [])
def p_unary_operator_3(t):
	'unary_operator : PLUS'
	t[0]=Node(t[1], [])
def p_unary_operator_4(t):
	'unary_operator : MINUS'
	t[0]=Node(t[1], [])
def p_unary_operator_5(t):
	'unary_operator : TILDA'
	t[0]=Node(t[1], [])
def p_unary_operator_6(t):
	'unary_operator : EXCLAMATION'
	t[0]=Node(t[1], [])
def p_cast_expression_1(t):
	'cast_expression : unary_expression'
	t[0]=t[1]
def p_cast_expression_2(t):
	'cast_expression : LEFT_ROUND type_name RIGHT_ROUND cast_expression'
	t[0]=Node('cast_expression', [t[2],t[4]])
def p_multiplicative_expression_1(t):
	'multiplicative_expression : cast_expression'
	t[0]=t[1]
def p_multiplicative_expression_2(t):
	'multiplicative_expression : multiplicative_expression MULTIPLY cast_expression'
	t[0]=Node('multiplicative_expression', [t[1],Node(t[2], []),t[3]])
def p_multiplicative_expression_3(t):
	'multiplicative_expression : multiplicative_expression DIVIDE cast_expression'
	t[0]=Node('multiplicative_expression', [t[1],Node(t[2], []),t[3]])
def p_multiplicative_expression_4(t):
	'multiplicative_expression : multiplicative_expression MODULO cast_expression'
	t[0]=Node('multiplicative_expression', [t[1],Node(t[2], []),t[3]])
def p_additive_expression_1(t):
	'additive_expression : multiplicative_expression'
	t[0]=t[1]
def p_additive_expression_2(t):
	'additive_expression : additive_expression PLUS multiplicative_expression'
	t[0]=Node('additive_expression', [t[1],Node(t[2], []),t[3]])
def p_additive_expression_3(t):
	'additive_expression : additive_expression MINUS multiplicative_expression'
	t[0]=Node('additive_expression', [t[1],Node(t[2], []),t[3]])
def p_shift_expression_1(t):
	'shift_expression : additive_expression'
	t[0]=t[1]
def p_shift_expression_2(t):
	'shift_expression : shift_expression LEFT_OP additive_expression'
	t[0]=Node('shift_expression', [t[1],Node(t[2], []),t[3]])
def p_shift_expression_3(t):
	'shift_expression : shift_expression RIGHT_OP additive_expression'
	t[0]=Node('shift_expression', [t[1],Node(t[2], []),t[3]])
def p_relational_expression_1(t):
	'relational_expression : shift_expression'
	t[0]=t[1]
def p_relational_expression_2(t):
	'relational_expression : relational_expression L_OP shift_expression'
	t[0]=Node('relational_expression', [t[1],Node(t[2], []),t[3]])
def p_relational_expression_3(t):
	'relational_expression : relational_expression G_OP shift_expression'
	t[0]=Node('relational_expression', [t[1],Node(t[2], []),t[3]])
def p_relational_expression_4(t):
	'relational_expression : relational_expression LE_OP shift_expression'
	t[0]=Node('relational_expression', [t[1],Node(t[2], []),t[3]])
def p_relational_expression_5(t):
	'relational_expression : relational_expression GE_OP shift_expression'
	t[0]=Node('relational_expression', [t[1],Node(t[2], []),t[3]])
def p_equality_expression_1(t):
	'equality_expression : relational_expression'
	t[0]=t[1]
def p_equality_expression_2(t):
	'equality_expression : equality_expression EQ_OP relational_expression'
	t[0]=Node('equality_expression', [t[1],Node(t[2], []),t[3]])
def p_equality_expression_3(t):
	'equality_expression : equality_expression NE_OP relational_expression'
	t[0]=Node('equality_expression', [t[1],Node(t[2], []),t[3]])
def p_and_expression_1(t):
	'and_expression : equality_expression'
	t[0]=t[1]
def p_and_expression_2(t):
	'and_expression : and_expression AMPERSAND equality_expression'
	t[0]=Node('and_expression', [t[1],Node(t[2], []),t[3]])
def p_exclusive_or_expression_1(t):
	'exclusive_or_expression : and_expression'
	t[0]=t[1]
def p_exclusive_or_expression_2(t):
	'exclusive_or_expression : exclusive_or_expression POWER and_expression'
	t[0]=Node('exclusive_or_expression', [t[1],Node(t[2], []),t[3]])
def p_inclusive_or_expression_1(t):
	'inclusive_or_expression : exclusive_or_expression'
	t[0]=t[1]
def p_inclusive_or_expression_2(t):
	'inclusive_or_expression : inclusive_or_expression PIPE exclusive_or_expression'
	t[0]=Node('inclusive_or_expression', [t[1],Node(t[2], []),t[3]])
def p_logical_and_expression_1(t):
	'logical_and_expression : inclusive_or_expression'
	t[0]=t[1]
def p_logical_and_expression_2(t):
	'logical_and_expression : logical_and_expression AND_OP inclusive_or_expression'
	t[0]=Node('logical_and_expression', [t[1],Node(t[2], []),t[3]])
def p_logical_or_expression_1(t):
	'logical_or_expression : logical_and_expression'
	t[0]=t[1]
def p_logical_or_expression_2(t):
	'logical_or_expression : logical_or_expression OR_OP logical_and_expression'
	t[0]=Node('logical_or_expression', [t[1],Node(t[2], []),t[3]])
def p_conditional_expression_1(t):
	'conditional_expression : logical_or_expression'
	t[0]=t[1]
def p_conditional_expression_2(t):
	'conditional_expression : logical_or_expression QUESTION expression COLON conditional_expression'
	t[0]=Node('conditional_expression', [t[1],Node(t[2], []),t[3],Node(t[4], []),t[5]])
def p_assignment_expression_1(t):
	'assignment_expression : conditional_expression'
	t[0]=t[1]
def p_assignment_expression_2(t):
	'assignment_expression : unary_expression assignment_operator assignment_expression'
	t[0]=Node('assignment_expression', [t[1],t[2],t[3]])
def p_assignment_operator_1(t):
	'assignment_operator : EQUAL'
	t[0]=Node(t[1], [])
def p_assignment_operator_2(t):
	'assignment_operator : MUL_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_3(t):
	'assignment_operator : DIV_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_4(t):
	'assignment_operator : MOD_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_5(t):
	'assignment_operator : ADD_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_6(t):
	'assignment_operator : SUB_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_7(t):
	'assignment_operator : LEFT_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_8(t):
	'assignment_operator : RIGHT_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_9(t):
	'assignment_operator : AND_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_10(t):
	'assignment_operator : XOR_ASSIGN'
	t[0]=Node(t[1], [])
def p_assignment_operator_11(t):
	'assignment_operator : OR_ASSIGN'
	t[0]=Node(t[1], [])
def p_expression_1(t):
	'expression : assignment_expression'
	t[0]=t[1]
def p_expression_2(t):
	'expression : expression COMMA assignment_expression'
	t[0]=Node('expression', [t[1],t[3]])
def p_constant_expression_1(t):
	'constant_expression : conditional_expression'
	t[0]=t[1]
def p_declaration_1(t):
	'declaration : declaration_specifiers SEMICOLON'
	t[0]=t[1]
def p_declaration_2(t):
	'declaration : declaration_specifiers init_declarator_list SEMICOLON'
	t[0]=Node('declaration', [t[1],t[2]])
def p_declaration_specifiers_1(t):
	'declaration_specifiers : storage_class_specifier'
	t[0]=t[1]
def p_declaration_specifiers_2(t):
	'declaration_specifiers : storage_class_specifier declaration_specifiers'
	t[0]=Node('declaration_specifiers', [t[1],t[2]])
def p_declaration_specifiers_3(t):
	'declaration_specifiers : type_specifier'
	t[0]=t[1]
def p_declaration_specifiers_4(t):
	'declaration_specifiers : type_specifier declaration_specifiers'
	t[0]=Node('declaration_specifiers', [t[1],t[2]])
def p_declaration_specifiers_5(t):
	'declaration_specifiers : type_qualifier'
	t[0]=t[1]
def p_declaration_specifiers_6(t):
	'declaration_specifiers : type_qualifier declaration_specifiers'
	t[0]=Node('declaration_specifiers', [t[1],t[2]])
def p_init_declarator_list_1(t):
	'init_declarator_list : init_declarator'
	t[0]=t[1]
def p_init_declarator_list_2(t):
	'init_declarator_list : init_declarator_list COMMA init_declarator'
	t[0]=Node('init_declarator_list', [t[1],t[3]])
def p_init_declarator_1(t):
	'init_declarator : declarator'
	t[0]=t[1]
def p_init_declarator_2(t):
	'init_declarator : declarator EQUAL initializer'
	t[0]=Node('init_declarator', [t[1],Node(t[2], []),t[3]])
def p_storage_class_specifier_1(t):
	'storage_class_specifier : TYPEDEF'
	t[0]=Node(t[1], [])
def p_storage_class_specifier_2(t):
	'storage_class_specifier : EXTERN'
	t[0]=Node(t[1], [])
def p_storage_class_specifier_3(t):
	'storage_class_specifier : STATIC'
	t[0]=Node(t[1], [])
def p_storage_class_specifier_4(t):
	'storage_class_specifier : AUTO'
	t[0]=Node(t[1], [])
def p_storage_class_specifier_5(t):
	'storage_class_specifier : REGISTER'
	t[0]=Node(t[1], [])
def p_type_specifier_1(t):
	'type_specifier : VOID'
	t[0]=Node(t[1], [])
def p_type_specifier_2(t):
	'type_specifier : CHAR'
	t[0]=Node(t[1], [])
def p_type_specifier_3(t):
	'type_specifier : SHORT'
	t[0]=Node(t[1], [])
def p_type_specifier_4(t):
	'type_specifier : INT'
	t[0]=Node(t[1], [])
def p_type_specifier_5(t):
	'type_specifier : LONG'
	t[0]=Node(t[1], [])
def p_type_specifier_6(t):
	'type_specifier : FLOAT'
	t[0]=Node(t[1], [])
def p_type_specifier_7(t):
	'type_specifier : DOUBLE'
	t[0]=Node(t[1], [])
def p_type_specifier_8(t):
	'type_specifier : SIGNED'
	t[0]=Node(t[1], [])
def p_type_specifier_9(t):
	'type_specifier : UNSIGNED'
	t[0]=Node(t[1], [])
def p_type_specifier_10(t):
	'type_specifier : struct_or_union_specifier'
	t[0]=t[1]
def p_type_specifier_11(t):
	'type_specifier : enum_specifier'
	t[0]=t[1]
def p_struct_or_union_specifier_1(t):
	'struct_or_union_specifier : struct_or_union IDENTIFIER LEFT_CURL struct_declaration_list RIGHT_CURL'
	t[0]=Node('struct_or_union_specifier', [t[1],Node(t[2], []),t[4]])
def p_struct_or_union_specifier_2(t):
	'struct_or_union_specifier : struct_or_union LEFT_CURL struct_declaration_list RIGHT_CURL'
	t[0]=Node('struct_or_union_specifier', [t[1],t[3]])
def p_struct_or_union_specifier_3(t):
	'struct_or_union_specifier : struct_or_union IDENTIFIER'
	t[0]=Node('struct_or_union_specifier', [t[1],Node(t[2], [])])
def p_struct_or_union_1(t):
	'struct_or_union : STRUCT'
	t[0]=Node(t[1], [])
def p_struct_or_union_2(t):
	'struct_or_union : UNION'
	t[0]=Node(t[1], [])
def p_struct_declaration_list_1(t):
	'struct_declaration_list : struct_declaration'
	t[0]=t[1]
def p_struct_declaration_list_2(t):
	'struct_declaration_list : struct_declaration_list struct_declaration'
	t[0]=Node('struct_declaration_list', [t[1],t[2]])
def p_struct_declaration_1(t):
	'struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON'
	t[0]=Node('struct_declaration', [t[1],t[2]])
def p_specifier_qualifier_list_1(t):
	'specifier_qualifier_list : type_specifier specifier_qualifier_list'
	t[0]=Node('specifier_qualifier_list', [t[1],t[2]])
def p_specifier_qualifier_list_2(t):
	'specifier_qualifier_list : type_specifier'
	t[0]=t[1]
def p_specifier_qualifier_list_3(t):
	'specifier_qualifier_list : type_qualifier specifier_qualifier_list'
	t[0]=Node('specifier_qualifier_list', [t[1],t[2]])
def p_specifier_qualifier_list_4(t):
	'specifier_qualifier_list : type_qualifier'
	t[0]=t[1]
def p_struct_declarator_list_1(t):
	'struct_declarator_list : struct_declarator'
	t[0]=t[1]
def p_struct_declarator_list_2(t):
	'struct_declarator_list : struct_declarator_list COMMA struct_declarator'
	t[0]=Node('struct_declarator_list', [t[1],t[3]])
def p_struct_declarator_1(t):
	'struct_declarator : declarator'
	t[0]=t[1]
def p_struct_declarator_2(t):
	'struct_declarator : COLON constant_expression'
	t[0]=Node('struct_declarator', [Node(t[1], []),t[2]])
def p_struct_declarator_3(t):
	'struct_declarator : declarator COLON constant_expression'
	t[0]=Node('struct_declarator', [t[1],Node(t[2], []),t[3]])
def p_enum_specifier_1(t):
	'enum_specifier : ENUM LEFT_CURL enumerator_list RIGHT_CURL'
	t[0]=Node('enum_specifier', [Node(t[1], []),t[3]])
def p_enum_specifier_2(t):
	'enum_specifier : ENUM IDENTIFIER LEFT_CURL enumerator_list RIGHT_CURL'
	t[0]=Node('enum_specifier', [Node(t[1], []),Node(t[2], []),t[4]])
def p_enum_specifier_3(t):
	'enum_specifier : ENUM IDENTIFIER'
	t[0]=Node('enum_specifier', [Node(t[1], []),Node(t[2], [])])
def p_enumerator_list_1(t):
	'enumerator_list : enumerator'
	t[0]=t[1]
def p_enumerator_list_2(t):
	'enumerator_list : enumerator_list COMMA enumerator'
	t[0]=Node('enumerator_list', [t[1],t[3]])
def p_enumerator_1(t):
	'enumerator : IDENTIFIER'
	t[0]=Node(t[1], [])
def p_enumerator_2(t):
	'enumerator : IDENTIFIER EQUAL constant_expression'
	t[0]=Node('enumerator', [Node(t[1], []),Node(t[2], []),t[3]])
def p_type_qualifier_1(t):
	'type_qualifier : CONST'
	t[0]=Node(t[1], [])
def p_type_qualifier_2(t):
	'type_qualifier : VOLATILE'
	t[0]=Node(t[1], [])
def p_declarator_1(t):
	'declarator : pointer direct_declarator'
	t[0]=Node('declarator', [t[1],t[2]])
def p_declarator_2(t):
	'declarator : direct_declarator'
	t[0]=t[1]
def p_direct_declarator_1(t):
	'direct_declarator : IDENTIFIER'
	t[0]=Node(t[1], [])
def p_direct_declarator_2(t):
	'direct_declarator : LEFT_ROUND declarator RIGHT_ROUND'
	t[0]=t[2]
def p_direct_declarator_3(t):
	'direct_declarator : direct_declarator LEFT_SQUARE constant_expression RIGHT_SQUARE'
	t[0]=Node('direct_declarator', [t[1],t[3]])
def p_direct_declarator_4(t):
	'direct_declarator : direct_declarator LEFT_SQUARE RIGHT_SQUARE'
	t[0]=Node('direct_declarator', [t[1],Node('parameter_type_list', [])])
def p_direct_declarator_5(t):
	'direct_declarator : direct_declarator LEFT_ROUND parameter_type_list RIGHT_ROUND'
	t[0]=Node('direct_declarator', [t[1],t[3]])
def p_direct_declarator_6(t):
	'direct_declarator : direct_declarator LEFT_ROUND identifier_list RIGHT_ROUND'
	t[0]=Node('direct_declarator', [t[1],t[3]])
def p_direct_declarator_7(t):
	'direct_declarator : direct_declarator LEFT_ROUND RIGHT_ROUND'
	t[0]=Node('direct_declarator', [t[1],Node('identifier_list', [])])
def p_pointer_1(t):
	'pointer : MULTIPLY'
	t[0]=Node(t[1], [])
def p_pointer_2(t):
	'pointer : MULTIPLY type_qualifier_list'
	t[0]=Node('pointer', [Node(t[1], []),t[2]])
def p_pointer_3(t):
	'pointer : MULTIPLY pointer'
	t[0]=Node('pointer', [Node(t[1], []),t[2]])
def p_pointer_4(t):
	'pointer : MULTIPLY type_qualifier_list pointer'
	t[0]=Node('pointer', [Node(t[1], []),t[2],t[3]])
def p_type_qualifier_list_1(t):
	'type_qualifier_list : type_qualifier'
	t[0]=t[1]
def p_type_qualifier_list_2(t):
	'type_qualifier_list : type_qualifier_list type_qualifier'
	t[0]=Node('type_qualifier_list', [t[1],t[2]])
def p_parameter_type_list_1(t):
	'parameter_type_list : parameter_list'
	t[0]=t[1]
def p_parameter_type_list_2(t):
	'parameter_type_list : parameter_list COMMA ELLIPSIS'
	t[0]=Node('parameter_type_list', [t[1],Node(t[3], [])])
def p_parameter_list_1(t):
	'parameter_list : parameter_declaration'
	t[0]=t[1]
def p_parameter_list_2(t):
	'parameter_list : parameter_list COMMA parameter_declaration'
	t[0]=Node('parameter_list', [t[1],t[3]])
def p_parameter_declaration_1(t):
	'parameter_declaration : declaration_specifiers declarator'
	t[0]=Node('parameter_declaration', [t[1],t[2]])
def p_parameter_declaration_2(t):
	'parameter_declaration : declaration_specifiers abstract_declarator'
	t[0]=Node('parameter_declaration', [t[1],t[2]])
def p_parameter_declaration_3(t):
	'parameter_declaration : declaration_specifiers'
	t[0]=t[1]
def p_identifier_list_1(t):
	'identifier_list : IDENTIFIER'
	t[0]=Node(t[1], [])
def p_identifier_list_2(t):
	'identifier_list : identifier_list COMMA IDENTIFIER'
	t[0]=Node('identifier_list', [t[1],Node(t[3], [])])
def p_type_name_1(t):
	'type_name : specifier_qualifier_list'
	t[0]=t[1]
def p_type_name_2(t):
	'type_name : specifier_qualifier_list abstract_declarator'
	t[0]=Node('type_name', [t[1],t[2]])
def p_abstract_declarator_1(t):
	'abstract_declarator : pointer'
	t[0]=t[1]
def p_abstract_declarator_2(t):
	'abstract_declarator : direct_abstract_declarator'
	t[0]=t[1]
def p_abstract_declarator_3(t):
	'abstract_declarator : pointer direct_abstract_declarator'
	t[0]=Node('abstract_declarator', [t[1],t[2]])
def p_direct_abstract_declarator_1(t):
	'direct_abstract_declarator : LEFT_ROUND abstract_declarator RIGHT_ROUND'
	t[0]=t[1]
def p_direct_abstract_declarator_2(t):
	'direct_abstract_declarator : LEFT_SQUARE RIGHT_SQUARE'
	t[0]=Node('abstract_declarator', [])
def p_direct_abstract_declarator_3(t):
	'direct_abstract_declarator : LEFT_SQUARE constant_expression RIGHT_SQUARE'
	t[0]=t[2]
def p_direct_abstract_declarator_4(t):
	'direct_abstract_declarator : direct_abstract_declarator LEFT_SQUARE RIGHT_SQUARE'
	t[0]=Node('direct_abstract_declarator', [t[1],Node('constant_expression', [])])
def p_direct_abstract_declarator_5(t):
	'direct_abstract_declarator : direct_abstract_declarator LEFT_SQUARE constant_expression RIGHT_SQUARE'
	t[0]=Node('direct_abstract_declarator', [t[1],t[3]])
def p_direct_abstract_declarator_6(t):
	'direct_abstract_declarator : LEFT_ROUND RIGHT_ROUND'
	t[0]=Node('parameter_type_list', [])
def p_direct_abstract_declarator_7(t):
	'direct_abstract_declarator : LEFT_ROUND parameter_type_list RIGHT_ROUND'
	t[0]=t[2]
def p_direct_abstract_declarator_8(t):
	'direct_abstract_declarator : direct_abstract_declarator LEFT_ROUND RIGHT_ROUND'
	t[0]=Node('direct_abstract_declarator', [t[1],Node('parameter_type_list', [])])
def p_direct_abstract_declarator_9(t):
	'direct_abstract_declarator : direct_abstract_declarator LEFT_ROUND parameter_type_list RIGHT_ROUND'
	t[0]=Node('direct_abstract_declarator', [t[1],t[3]])
def p_initializer_1(t):
	'initializer : assignment_expression'
	t[0]=t[1]
def p_initializer_2(t):
	'initializer : LEFT_CURL initializer_list RIGHT_CURL'
	t[0]=t[2]
def p_initializer_3(t):
	'initializer : LEFT_CURL initializer_list COMMA RIGHT_CURL'
	t[0]=t[2]
def p_initializer_list_1(t):
	'initializer_list : initializer'
	t[0]=t[1]
def p_initializer_list_2(t):
	'initializer_list : initializer_list COMMA initializer'
	t[0]=Node('initializer_list', [t[1],t[3]])
def p_statement_1(t):
	'statement : labeled_statement'
	t[0]=t[1]
def p_statement_2(t):
	'statement : compound_statement'
	t[0]=t[1]
def p_statement_3(t):
	'statement : expression_statement'
	t[0]=t[1]
def p_statement_4(t):
	'statement : selection_statement'
	t[0]=t[1]
def p_statement_5(t):
	'statement : iteration_statement'
	t[0]=t[1]
def p_statement_6(t):
	'statement : jump_statement'
	t[0]=t[1]
def p_labeled_statement_1(t):
	'labeled_statement : IDENTIFIER COLON statement'
	t[0]=Node('labeled_statement', [Node(t[1], []),Node(t[2], []),t[3]])
def p_labeled_statement_2(t):
	'labeled_statement : CASE constant_expression COLON statement'
	t[0]=Node('labeled_statement', [Node(t[1], []),t[2],Node(t[3], []),t[4]])
def p_labeled_statement_3(t):
	'labeled_statement : DEFAULT COLON statement'
	t[0]=Node('labeled_statement', [Node(t[1], []),Node(t[2], []),t[3]])
def p_compound_statement_1(t):
	'compound_statement : LEFT_CURL RIGHT_CURL'
	t[0]=Node('statement_list', [])
def p_compound_statement_2(t):
	'compound_statement : LEFT_CURL statement_list RIGHT_CURL'
	t[0]=t[2]
def p_compound_statement_3(t):
	'compound_statement : LEFT_CURL declaration_list RIGHT_CURL'
	t[0]=t[2]
def p_compound_statement_4(t):
	'compound_statement : LEFT_CURL declaration_list statement_list RIGHT_CURL'
	t[0]=Node('compound_statement', [t[2],t[3]])
def p_declaration_list_1(t):
	'declaration_list : declaration'
	t[0]=t[1]
def p_declaration_list_2(t):
	'declaration_list : declaration_list declaration'
	t[0]=Node('declaration_list', [t[1],t[2]])
def p_statement_list_1(t):
	'statement_list : statement'
	t[0]=t[1]
def p_statement_list_2(t):
	'statement_list : statement_list statement'
	t[0]=Node('statement_list', [t[1],t[2]])
def p_expression_statement_1(t):
	'expression_statement : SEMICOLON'
	t[0]=Node(t[1], [])
def p_expression_statement_2(t):
	'expression_statement : expression SEMICOLON'
	t[0]=t[1]
def p_selection_statement_1(t):
	'selection_statement : IF LEFT_ROUND expression RIGHT_ROUND statement %prec else_priority'
	t[0]=Node('selection_statement', [Node(t[1], []),t[3],t[5]])
def p_selection_statement_2(t):
	'selection_statement : IF LEFT_ROUND expression RIGHT_ROUND statement ELSE statement'
	t[0]=Node('selection_statement', [Node(t[1], []),t[3],t[5],Node(t[6], []),t[7]])
def p_selection_statement_3(t):
	'selection_statement : SWITCH LEFT_ROUND expression RIGHT_ROUND statement'
	t[0]=Node('selection_statement', [Node(t[1], []),t[3],t[5]])
def p_iteration_statement_1(t):
	'iteration_statement : WHILE LEFT_ROUND expression RIGHT_ROUND statement'
	t[0]=Node('iteration_statement', [Node(t[1], []),t[3],t[5]])
def p_iteration_statement_2(t):
	'iteration_statement : DO statement WHILE LEFT_ROUND expression RIGHT_ROUND SEMICOLON'
	t[0]=Node('iteration_statement', [Node(t[1], []),t[2],Node(t[3], []),t[5]])
def p_iteration_statement_3(t):
	'iteration_statement : FOR LEFT_ROUND expression_statement expression_statement RIGHT_ROUND statement'
	t[0]=Node('iteration_statement', [Node(t[1], []),t[3],t[4],t[6]])
def p_iteration_statement_4(t):
	'iteration_statement : FOR LEFT_ROUND expression_statement expression_statement expression RIGHT_ROUND statement'
	t[0]=Node('iteration_statement', [Node(t[1], []),t[3],t[4],t[5],t[7]])
def p_jump_statement_1(t):
	'jump_statement : GOTO IDENTIFIER SEMICOLON'
	t[0]=Node('jump_statement', [Node(t[1], []),Node(t[2], [])])
def p_jump_statement_2(t):
	'jump_statement : CONTINUE SEMICOLON'
	t[0]=Node(t[1], [])
def p_jump_statement_3(t):
	'jump_statement : BREAK SEMICOLON'
	t[0]=Node(t[1], [])
def p_jump_statement_4(t):
	'jump_statement : RETURN SEMICOLON'
	t[0]=Node(t[1], [])
def p_jump_statement_5(t):
	'jump_statement : RETURN expression SEMICOLON'
	t[0]=Node('jump_statement', [Node(t[1], []),t[2]])
def p_translation_unit_1(t):
	'translation_unit : external_declaration'
	t[0]=t[1]
def p_translation_unit_2(t):
	'translation_unit : translation_unit external_declaration'
	t[0]=Node('translation_unit', [t[1],t[2]])
def p_external_declaration_1(t):
	'external_declaration : function_definition'
	t[0]=t[1]
def p_external_declaration_2(t):
	'external_declaration : declaration'
	t[0]=t[1]
def p_function_definition_1(t):
	'function_definition : declaration_specifiers declarator declaration_list compound_statement'
	t[0]=Node('function_definition', [t[1],t[2],t[3],t[4]])
def p_function_definition_2(t):
	'function_definition : declaration_specifiers declarator compound_statement'
	t[0]=Node('function_definition', [t[1],t[2],t[3]])
def p_function_definition_3(t):
	'function_definition : declarator declaration_list compound_statement'
	t[0]=Node('function_definition', [t[1],t[2],t[3]])
def p_function_definition_4(t):
	'function_definition : declarator compound_statement'
	t[0]=Node('function_definition', [t[1],t[2]])

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
