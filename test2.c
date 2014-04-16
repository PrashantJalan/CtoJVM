#include<stdio.h>

void foo(int a[10], int b)	{
	a[9] = b;
	int x=2;
	float z,e,r=2.2;
	z = 2.5;
	int y=2;
	e = y*z + r;
	int c = a[9];
	print e;
}
void main()
{
int a[10];
foo(a, 5*6/3);
}


