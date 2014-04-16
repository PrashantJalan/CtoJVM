
void foo()
{
static int count;
count = count+2;
print count;
}

void main()
{
int i;
for(i=0;i<5;i=i+1)
	{
	foo();
	}
}