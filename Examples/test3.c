//Convulution Code

void convolve(int inp[10][8], int kernel[3][3], int out[10][8], int row, int col, int kern){
	int i, j, k, iter, sum=0, data=0, coeff=0;
	for (i = 0; i < row; ++i)
	{
		for (j = 0; j < col; ++j)
		{
			sum=0;
			for (k = 0; k < kern; ++k)
			{
				if (row - i < kern)
				{
					break;
				}
				for (iter = 0; iter < kern; ++iter)
				{
					if (col - j < kern)
					{
						break;
					}
					sum+=inp[k+i][iter+j] * kernel[k][iter];
				}
			}
			if(i < row && j < col){
				out[i][j]=sum;
			}
		}
	}
}

void main(){
	int col=8, row=10, kern=3, i=0, j=0, k=0;  //inp[m,n]; kernel[k, k]; out[]
	int inp[10][8], kernel[3][3], out[10][8];
	for (i = 0; i < row; ++i)
	{
		for (j = 0; j < col; ++j)
		{
			inp[i][j]=i*j;
		}
	}
	for (i = 0; i < kern; ++i)
	{
		for (j = 0; j < kern; ++j)
		{
			kernel[i][j]=2;
		}
	}
	convolve(inp, kernel, out, row, col, kern);
	for (i = 0; i < row-kern+1; ++i)
	{
		for (j = 0; j < col-kern+1; ++j)
		{
			int t;
			t= out[i][j];
			print t;
		}
	}
}