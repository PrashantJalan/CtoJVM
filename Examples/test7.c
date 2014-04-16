//error checking

#include <stdio.h>
void main(){
	char a;
	int b=10;
	//a = b;			//assigning an integer value to a char.

	int x=2;
	float y=2.3;

	int p;
	float q;

	//p = x+y;		//Assignment error
	q = x+y;		//type casting

	print q;

	float m=2.3;
	char c;
	//b=m+c;		//char cannot add to float
}