#include <limits.h>
/*@
    assigns \nothing;
    ensures \result >= INT_MIN && \result <= INT_MAX;
*/
int unknown_int();

/*@
  assigns \nothing;
  ensures \result == 0;
*/
int main() {
  int n,i,k;
  n = unknown_int();
  k = n;
  i = 0;

  /*@
    loop invariant 0 <= i;
    loop invariant i % 2 == 0;
    loop invariant i <= n + 1 || n < 0;
    loop invariant k == n - i/2;
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
    loop invariant 0 <= j;
    loop invariant k == n - i/2 - j;
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
