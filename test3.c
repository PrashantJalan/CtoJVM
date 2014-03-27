#include<stdio.h>

int main()
{
int t,i,j,n,k,flag,res,match;
char ch[20000];

for(i=0;i<t;i++)
	{
	flag=0;
	res=0;
	match=1;
	for(j=1;j<n;j++)
		{
		if(ch[j]==ch[j-1] && match<k)
			match++;
		else
			{
			res++;
			if(match==k)
				flag=1;
			match=1;
			}
		}
	res++;
	if(match==k)
		flag=1;
	}
return 0;
}
