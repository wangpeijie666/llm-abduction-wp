#include "assert.h"

#define SZ 2048

int main(void) {
  int A[SZ];
  int B[SZ];
  int i;
  int tmp;

  /*@
    loop invariant 0 <= i <= SZ;
    loop invariant \forall integer j; 0 <= j < i ==> B[j] == A[j];
    loop assigns i, tmp, B[0..2047];
  */
  /* PROBE_HERE:loop1_before */
  for (i = 0; i < SZ; i++) {
    /* PROBE_HERE:loop1_body_entry */
    tmp = A[i];
    B[i] = tmp;
  }

  //@ assert(A[SZ/2] == B[SZ/2]);
}
