#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*
 * from Invgen test suite
 */
/*@
requires n > 0;
requires k > n;
assigns \nothing;
ensures \result == 0;
*/
int foo(int n, int k) {

  int i, j;

  j = 0;
  /*@
    loop invariant 0 <= j <= n;
    loop invariant k == \at(k,Pre) - j;
    loop invariant k > n - j;
    loop assigns j, k;
  */
  /* PROBE_HERE:loop1_before */
  while( j < n ) {
    /* PROBE_HERE:loop1_body_entry */
    j++;
    k--;
  } 
  //@ assert(k>=0);
  return 0;
}
