#include "assert.h"

#define SZ 2048

/*@
  requires \valid(A + (0 .. SZ-1));
  requires \valid(B + (0 .. SZ-1));
  ensures \forall integer k; 0 <= k < SZ ==> A[k] == B[k];
*/
int main(void) {
  int A[SZ];
  int B[SZ];
  int i;
  int tmp;

  /*@
    loop invariant 0 <= i <= SZ;
    loop invariant \forall integer k; 0 <= k < i ==> A[k] == B[k];
    loop assigns i, tmp, B[0 .. SZ-1];
  */
  for (i = 0; i < SZ; i++) {
    tmp = A[i];
    B[i] = tmp;
  }

  //@ assert A[SZ/2] == B[SZ/2];
}
