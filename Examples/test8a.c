//This code shows that our compiler will not parse incorrect syntax

#include <stdio.h>
void int(int a){ 				//using reserved keyword for a function name.
	int a=9;
	print a;
}
void func(int c){ 				//checking for error when the type of actual and formal parameter should match.
	int a=0;
	print a;
}

void main(){
	int c=10;
	int l, m, n=0;
	char arr['c'];				//using wrong data type for array index.
	int a   					//semicolon is missing.
	a=100;
	print a;
	l+m=n; 						//more than one operand on the LHS of an assignment.
	int(c);
	func(c);
}