float foo(float a[10])	{
	a[9] = 56.2343;
	return a[9];
}
void main()
{
float a[10];
float z = foo(a);
print z;
}


