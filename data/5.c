void swap(int x,int y)
{
  int temp;
  temp=x;
  x=y;
  y=temp;
}

int mod(int x,int y) 
{
  return (x-x/y*y);
}

void main()
{
  int a,b,c,temp1,temp2,result_1,result_2;
  printf("Input a : ");
  scanf(a);
  printf("Input b : ");
  scanf(b);	
  temp1=a;
  temp2=b;
  if (temp1!=0)
  {
     printf("temp1 = ",temp1);
     printf("temp2 = ",temp2);
     swap(temp1,temp2);
     printf("temp1 = ",temp1);
     printf("temp2 = ",temp2);
     c= mod(a,b);
     printf("mod(a,b) = ", c);
  }
  result_1=temp2;
  result_2=a*b/result_1;
  printf(result_1);
  printf(result_2);
}