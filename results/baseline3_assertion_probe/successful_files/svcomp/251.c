#include <limits.h>
/*@
  ensures 0 <= \result <= INT_MAX;
  assigns \nothing;
*/
int unknown_int();

int main() {
  int n;
  int i = 0;
  int k = 0;
  n = unknown_int();
  /*@
    loop invariant 0 <= i && i <= n;
    loop invariant k == i;
    loop assigns i, k;
  */
  /* PROBE_HERE:loop1_before */
  while( i < n ) {
    /* PROBE_HERE:loop1_body_entry */
    i++;
    k++;
  }

  int j = 0;
  /*@
    loop invariant 0 <= j <= n;
    loop invariant k == n - j;
    loop assigns j, k;
  */
  /* PROBE_HERE:loop2_before */
  while( j < n ) {
    /* PROBE_HERE:loop2_body_entry */
    //@ assert (k > 0);
    j++;
    k--;
  }
}
