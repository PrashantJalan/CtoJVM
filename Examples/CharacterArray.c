char foo(char a[10])	{
	a[9] = 'a';
	return a[9];
}

void main()
{
	char a[10];
	char z = foo(a);
	print z;
}