//Recursive Fibonacci

int fib(int n);

int fib(int n)	{
	int x,y,z,p,q;

	if (n==0)	{
		z = 0;
	}
	else if (n==1)	{
		z = 1;
	}
	else	{
		p = n-1;
		q = n-2;
		x = fib(p);
		y = fib(q);
		z = x+y;
	}
	return z;
}
void main()
{
	int x;
	x = fib(7);
	print x;
}