#include <assert.h>
/*@
ensures \result >= 0;
assigns \nothing;
*/
int unknown1();
/*@
assigns \nothing;
*/
int unknown2();
/*@
assigns \nothing;
*/
int unknown3();
/*@
assigns \nothing;
*/
int unknown4();

/*
 * Adapted from "Automated Error Diagnosis Using Abductive Inference" by Dillig et al.
 */
/*@
requires n > 0;
assigns \nothing;
*/
void foo(int n, int flag) {
  int k = 1;
  if (flag) {
    k = unknown1();
  }
  int i = 0, j = 0;
  /*@
    loop invariant 0 <= i <= n + 1;
    loop invariant 2*j == i*(i+1);
    loop assigns i, j;
  */
  /* PROBE_HERE:loop1_before */
  while (i <= n) {
    /* PROBE_HERE:loop1_body_entry */
    i++;
    j += i;
  }
  int z = k + i + j;
  //@ assert(z > 2 * n);
}
