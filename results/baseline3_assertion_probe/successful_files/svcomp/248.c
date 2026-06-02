#include <limits.h>
/*@
    assigns \nothing;
    ensures \result >= INT_MIN && \result <= INT_MAX;
*/
int unknown_int();

/*@
  assigns \nothing;
*/
int main() {
  int n0, n1;
  int i0 = 0;
  int k = 0;

  n0 = unknown_int();
  n1 = unknown_int();

  /*@
    loop invariant k == i0;
    loop invariant i0 >= 0;
    loop assigns i0, k;
  */
  /* PROBE_HERE:loop1_before */
  while( i0 < n0 ) {
    /* PROBE_HERE:loop1_body_entry */
    i0++;
    k++;
  }

  int i1 = 0;
  /*@
    loop invariant k == i0 + i1;
    loop invariant i1 >= 0;
    loop assigns i1, k;
  */
  /* PROBE_HERE:loop2_before */
  while( i1 < n1 ) {
    /* PROBE_HERE:loop2_body_entry */
    i1++;
    k++;
  }

  int j1 = 0;
  /*@
    loop invariant j1 >= 0;
    loop invariant k == i0 + i1 - j1;
    loop assigns j1, k;
  */
  /* PROBE_HERE:loop3_before */
  while( j1 < n0 + n1 ) {
      /* PROBE_HERE:loop3_body_entry */
      //@ assert(k > 0);
      j1++;
      k--;
  }
}
