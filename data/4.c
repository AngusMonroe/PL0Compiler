void main()
{
  int a,b;
  
  printf("Input a :"); 
  scanf(a);
  printf("Input b :"); 
  scanf(b);
  
  while ( b != 0 )
  {
    printf("a+b=",a+b);
    printf("a-b=",a-b);
    printf("a*b=",a*b);
    printf("a/b=",a/b);
    printf("Input a :"); 
    scanf(a);
    printf("Input b :"); 
    scanf(b);
  }
}
