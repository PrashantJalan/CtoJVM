#include<stdio.h>

void foo(int a[10])	{
	a[9] = 56;
	int c = a[9];
	print c;
}
void main()
{
int a[10];
foo(a);
}


