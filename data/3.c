const e=2, UPPER=200;
int power(int x) 
{
   int result, i;
   result=1;
   
   if (x<=0) 
      return (0);
   i=1;
   while(i<=x)
   { 
      result=result*e;
      i=i+1;
   }
   return (result);
}

void main()
{
   int number, test;
   printf("Input a number:");
   scanf(number);
   test=power(number);
   printf(test);
   if (test<UPPER) 
     printf("less than upper_line",UPPER-test);
   else
     printf("more than upper_line",test-UPPER);
   printf("Now we test the nagtive-parameter:");
   printf(power(-1));
}