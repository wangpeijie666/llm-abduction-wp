#include <limits.h>
/*@
    ensures \result > 0 && \result <= INT_MAX;
    assigns \nothing;
*/
int unknown_int();

int main() {
  int i, k, n, l;

  n = unknown_int();
  l = unknown_int();

  /*@
      loop invariant 1 <= k <= n;
      loop invariant l >= 0;
      loop invariant n > 0;
      loop assigns k, l;
  */
  for (k = 1; k < n; k++) {
    /*@
        loop invariant l <= i <= n;
        loop invariant 1 <= i;
        loop assigns i;
        loop variant n - i;
    */
    for (i = l; i < n; i++) {
      //@ assert 1 <= i;
    }

    if (unknown_int()) {
      l = l + 1;
    }
  }
}
