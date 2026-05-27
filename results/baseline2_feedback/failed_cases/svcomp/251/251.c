#include <limits.h>
/*@
  ensures INT_MIN <= \result <= INT_MAX;
*/
int unknown_int();

int main() {
  int n;
  int i = 0;
  int k = 0;
  n = unknown_int();

  /*@
    loop invariant 0 <= i;
    loop invariant n>=0==>i <= n;
    loop invariant k == i;
    loop assigns i, k;
    loop variant n - i;
  */
  while( i < n ) {
    i++;
    k++;
  }

  int j = 0;
  /*@
    loop invariant 0 <= j;
    loop invariant n>=0==>j <= n;
    loop invariant k == n - j;
    loop assigns j, k;
    loop variant n - j;
  */
  while( j < n ) {
    //@ assert (k > 0);
    j++;
    k--;
  }
}
