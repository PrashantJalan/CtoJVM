//This code shows the additional syntax checking


int foo()
{
int a=5;
}

void main()
{
float a=2.3;
int b=4;

a=a%2;		// modulo not defined for float
a=a++;		//unary not defined for float

if(b>2)
{
	b=4;
	break;	// break not in loop
}

}