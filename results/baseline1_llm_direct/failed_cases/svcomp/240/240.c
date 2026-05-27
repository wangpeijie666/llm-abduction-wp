#include <limits.h>
/*@
    ensures \result >= INT_MIN && \result <= INT_MAX;
*/
int unknown_int();

int main() {
  int n, i, k;
  n = unknown_int();
  k = n;
  i = 0;

  /*@
    loop invariant 0 <= i;
    loop invariant i <= n;
    loop invariant k == n - i / 2;
    loop assigns i, k;
  */
  while (i < n) {
    k--;
    i = i + 2;
  }

  int j = 0;

  /*@
    loop invariant 0 <= j;
    loop invariant j <= n / 2;
    loop invariant k == n - i / 2 - j;
    loop assigns j, k;
  */
  while (j < n / 2) {
    //@ assert k > 0;
    k--;
    j++;
  }

  return 0;
}
