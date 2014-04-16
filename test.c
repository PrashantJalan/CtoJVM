float foo(int a[10])	{
	a[9] = 56;
	int c = a[9];
	float d = 8.994;
	print d;
	return d;
}
void main()
{
int a[10];
float z = foo(a);
print z;
}


