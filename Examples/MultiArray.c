void foo(int x[10][5][4])
{
    int z;
    z = x[1][2][3];
    print z;
}

void main()
{
int a[10][5][4],b;
a[1][2][3]=12;
a[1][2][3]%=5;
b=a[1][2][3];
print b;
foo(a);
}