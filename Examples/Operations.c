//This code shows various operators supported

void main()
{
int a=2,b=2,c=2;
int x[20];


a+=2;
b-=2;
c*=2;
c++;

print a;
print b;
print c;


x[0]=10;
x[0]%=2;

c=x[0];
print c;


a = 2;
b = 3;
c = 4;

if(a<b && b<c)
	print a;
else if(a>=b || a>=c)
	print c;
else
	print b;
}