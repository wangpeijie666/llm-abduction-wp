#include<limits.h>

/*@
  assigns \nothing;
  ensures \result == (p*n*r)/100;
*/
int simple(int p,int n,int r)
{
    int si;
    si = p*n*r/100;
    return si;
}
 
/*@
  ensures \result == 0;
*/
int main()
{
    int s = simple(10000, 3,10);
    //@ assert s == 3000;
    return 0;
}
