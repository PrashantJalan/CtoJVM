//Saxpy implementation

void saxpy(int a[10], int b[10], int c[10], int alpha){
	int i;
	for(i=0;i<10;i++){
		c[i]=a[i]+alpha*b[i];
	}
	return;
}
void main(){
	int a[10], b[10], c[10], alpha=2, i=0, temp;
	
	for(i=0;i<10;i++){
		a[i]=i;
		b[i]=2*i;
	}
	saxpy(a, b, c, alpha);

	for(i=0;i<10;i++){
		temp = c[i];
		print temp;
	}
}