#include<stdio.h>

void foo(int a[10], int b)	{
	a[9] = b;
	int c = a[9];
	print c;
}
void main()
{
int a[10];
foo(a, 5*6/3);
}


