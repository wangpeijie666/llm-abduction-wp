#include <limits.h>
/*@
    ensures \result >= 0 && \result <= INT_MAX;
    assigns \nothing;
*/
int unknown_int();

int main() {
  int n0, n1;
  int i0 = 0;
  int k = 0;

  n0 = unknown_int();
  n1 = unknown_int();

  /*@
      loop invariant 0 <= i0 && i0 <= n0;
      loop invariant k == i0;
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
      loop invariant 0 <= i1 <= n1;
      loop invariant k == i0 + i1;
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
      loop invariant 0 <= j1 <= n0 + n1;
      loop invariant k == n0 + n1 - j1;
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
