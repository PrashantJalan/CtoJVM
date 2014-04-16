// Repeated and nested condition and number within a range

/*
Supports comments
*/

void main(){
	int a=100, up=5, low=-20;
	int z = 0;
	if(z <= a){
		if (z<up && z>low)
			print z;
		else if (z<=low)
			print low;
		else
			print up;
	}
	else
		print a;
}