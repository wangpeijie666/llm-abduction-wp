#include <assert.h>

/*
 * "nested4.c" from InvGen benchmark suite
 */

/*@
  requires l > 0;
  requires n > l;
  assigns \nothing;
*/
void foo(int n, int l) {
  int i,k;


  /*@
    loop invariant 1 <= k <= n;
    loop assigns k, i;
  */
  /* PROBE_HERE:loop1_before */
  for (k=1; k<n; k++){
    /* PROBE_HERE:loop1_body_entry */
    /*@
      loop invariant l <= i <= n;
      loop assigns i;
    */
    /* PROBE_HERE:loop2_before */
    for (i=l; i<n; i++) {
        /* PROBE_HERE:loop2_body_entry */
    }
    /*@
      loop invariant l <= i <= n;
      loop invariant l > 0;
      loop assigns i;
    */
    /* PROBE_HERE:loop3_before */
    for (i=l; i<n; i++) {
      /* PROBE_HERE:loop3_body_entry */
      //@ assert(1<=i);
    }
  }

}
