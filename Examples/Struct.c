struct Point2D{
int x;
int y;
char id;
};

void main()
{
struct Point2D point1;
struct Point2D point2;

struct Point2D point3;

point1.x = 1;
point1.y = 2;
point1.id = 'a';

point2.x = 2;
point2.y = 3;
point2.id = 'b';

point3.x = point1.x - point2.x;
point3.y = point1.y - point2.y;
point3.id = 'c';

int a,b;
char c;

a = point3.x;
b = point3.y;
c = point3.id;

print a;
print b;
print c;

}


