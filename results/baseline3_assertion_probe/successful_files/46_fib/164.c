#include <assert.h>
int unknown1();

/*@
  assigns \nothing;
*/
int unknown1();

/*
 * "nest-if8" from InvGen benchmark suite
 */

/*@
  assigns \nothing;
*/
void main() {
  int i, j, k, n, m;
  if (m + 1 < n);
  else return;
  /*@
    loop invariant 0 <= i;
    loop assigns i, j, k;
  */
  /* PROBE_HERE:loop1_before */
  for (i = 0; i < n; i += 4) {
    /* PROBE_HERE:loop1_body_entry */
    /*@
      loop invariant i <= j;
      loop invariant m + 1 < n;
      loop assigns j, k;
    */
    /* PROBE_HERE:loop2_before */
    for (j = i; j < m;) {
      /* PROBE_HERE:loop2_body_entry */
      if (unknown1()) {
        //@ assert(j >= 0);
        j++;
        k = 0;
        /*@
          loop invariant 0 <= k <= j;
          loop assigns k;
        */
        /* PROBE_HERE:loop3_before */
        while (k < j) {
          /* PROBE_HERE:loop3_body_entry */
          k++;
        }
      } else {
        //@ assert(n + j + 5 > i);
        j += 2;
      }
    }
  }
}
