#include <limits.h>
/*@
    ensures \result > 0 && \result <= INT_MAX;
*/
int unknown_int();

int main() {
  int i, k, n, l;

  n = unknown_int();
  l = unknown_int();
  /*@
    loop invariant 1 <= k;
    loop invariant k <= n;
    loop assigns k, i, l;
  */
  for (k = 1; k < n; k++) {
    /*@
      loop invariant l <= i;
      loop invariant i <= n;
      loop invariant 1 <= i || l < n;
      loop assigns i;
    */
    for (i = l; i < n; i++) {  
      //@ assert 1 <= i;
    }
    if (unknown_int()) {
      l = l + 1;
    }
  }
}
