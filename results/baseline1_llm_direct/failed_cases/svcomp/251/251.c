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
    loop invariant i <= n || n < 0;
    loop invariant k == i;
    loop assigns i, k;
  */
  while( i < n ) {
    i++;
    k++;
  }

  int j = 0;
  /*@
    loop invariant 0 <= j;
    loop invariant j <= n || n < 0;
    loop invariant k == n - j;
    loop assigns j, k;
  */
  while( j < n ) {
    //@ assert (k > 0);
    j++;
    k--;
  }
}
