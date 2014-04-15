
void main()
{
	int i, j, A[10], temp;

	for (i=0; i<10; i++)	{
		A[i] = 10-i;
	}

	for (i=0; i<10; i++)	{
		for (j=0; j<10-i-1; j++)	{
			if (A[j]>A[j+1])	{
				temp = A[j];
				A[j] = A[j+1];
				A[j+1] = temp;
			}
		}
	}

	for (i=0; i<10; i++)	{
		j = A[i];
		print j;
	}
}


