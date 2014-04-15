#include<stdio.h>

/**
int main()
{
   int n, first, second , next, c;
 
first=0;
second=1;
n=10;
 
   for ( c = 0 ; c < n ;c++ )
   {
      if ( c <= 1 )
         next = c;
      else
      {
         next = first + second;
         first = second;
         second = next;
      }
      print next;
   }
 
   return;
}

*/
void f02 (){
	int a;
}

int foo(int a, int b[3])	{
	return 0;
}
int main()
{
	int a,b,c;
	
	a=0;
	b=0;
	c=0;
	for(a=0;a<=10;a=a+1)
		{
		if(a  %2==0 )
			b = b+1;
		else
			c = c+1;
		}
	print b;
	print c;
	return;
}


