#include "assert.h"

int main(void) {
  int A[2048];
  int i;

  /*@
    loop invariant 0 <= i <= 1024;
    loop invariant \forall integer k; 0 <= k < i ==> A[k] == k;
    loop assigns i, A[0..1023];
  */
  for (i = 0; i < 1024; i++) {
    A[i] = i;
  }

  //@ assert(A[1023] == 1023);
}
