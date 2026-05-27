#include <limits.h>
/*@
    ensures \result >= INT_MIN && \result <= INT_MAX;
    assigns \nothing;
*/
int unknown_int();

int main() {
  int n,i,k;
  n = unknown_int();
  k = n;
  i = 0;

  /*@
    loop invariant 0 <= i <= n;
    loop invariant k == n - i / 2;
    loop assigns i, k;
  */
  /* PROBE_HERE:loop1_before */
  while( i < n ) {
    /* PROBE_HERE:loop1_body_entry */
    k--;
    i = i + 2;
  }

  int j = 0;
 
  /*@
    loop invariant 0 <= j <= n / 2;
    loop invariant k == n - i / 2 - j;
    loop assigns j, k;
  */
  /* PROBE_HERE:loop2_before */
  while( j < n/2 ) {
    /* PROBE_HERE:loop2_body_entry */
    //@ assert(k > 0);
    k--;
    j++;
  }
  return 0;
}
