//Scope Checking

int a;

void foo()
{
	a = 5;
	print a;
}

void main()
{
	foo();
	int a=10;
	int z[10];
	print a;

	//Error Checking
	
	//char a;				//redeclared
	//sort();				//function not declared
	//a();					//not declared as function
	//foo(2);				//mismatch arguments
	//z[2][1] = 5;			//mismatch array index
	//b = 5;				//not declared
}