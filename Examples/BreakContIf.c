void main()
{
int a=1;

if(a=2)			//THIS IS ALLOWED IN C
{
	a=2;
	//break;	//Check the error by uncommenting
}

while(a<10)
{
	a=a+1;
	if(a>=5)
	{
		break;
	}
}
print a;
}