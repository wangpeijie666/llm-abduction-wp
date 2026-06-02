#include <assert.h>

/*
 * "split.c" from InvGen benchmark suite
 */

void main() {
  int k = 100;
  int b;
  int i;
  int j;
  int n;
  i = j;
  /*@
    loop invariant 0 <= n <= 2*k;
    loop invariant \true;
    loop invariant (n % 2 == 0) ==> i == j;
    loop invariant (n % 2 == 1) ==> (i == j + 1 || j == i + 1);
    loop assigns n, i, j, b;
  */
  /* PROBE_HERE:loop1_before */
  for( n = 0 ; n < 2*k ; n++ ) {
    /* PROBE_HERE:loop1_body_entry */
    if(b) {
      i++;
    } else {
      j++;
    }
    b = !b;
  }
  //@ assert(i == j);
}
