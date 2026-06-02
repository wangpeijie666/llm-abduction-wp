#include <limits.h>

/*@
  assigns \nothing;
  ensures (x >= y ==> \result == x) && (x < y ==> \result == y);
  ensures \result >= x && \result >= y;
  ensures \result == x || \result == y;
*/
int max ( int x, int y ) {
    if ( x >=y ) 
        return x ;
    return y ;
}

/*@
  assigns \nothing;
*/
void foo()
{
    int s = max(34,45);
    //@ assert s==45;
    int t = max(-43,34);
    //@ assert t==34;
}
