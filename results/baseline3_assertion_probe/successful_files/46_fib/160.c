#include <assert.h>

/*
  * "nested2.c" from InvGen benchmark suite
  */
/*@
  requires l > 0;
  assigns \nothing;
*/
void foo(int l) {
  int i, k, n;

  /*@
    loop invariant 1 <= k;
    loop assigns k, i;
  */
  /* PROBE_HERE:loop1_before */
  for (k = 1; k < n; k++) {
    /* PROBE_HERE:loop1_body_entry */
    /*@
      loop invariant l <= i;
      loop assigns i;
    */
    /* PROBE_HERE:loop2_before */
    for (i = l; i < n; i++) {
        /* PROBE_HERE:loop2_body_entry */

    }
    /*@
      loop invariant l <= i;
      loop assigns i;
    */
    /* PROBE_HERE:loop3_before */
    for (i = l; i < n; i++) {
      /* PROBE_HERE:loop3_body_entry */
      //@ assert(1 <= k);
    }
  }

}
