const PI=3;
int radius,area,perimeter;
void main() 
{
     printf("Please input radius:");
     scanf (radius);
     if (radius<0) 
	printf("Error Input,try again!");
     else
     {
        printf(radius);
        perimeter=2*PI*radius;
	area=PI*radius*radius;
     }
     printf("This is a program that compute Circle's Area and Perimeter.");
     printf (area);
}