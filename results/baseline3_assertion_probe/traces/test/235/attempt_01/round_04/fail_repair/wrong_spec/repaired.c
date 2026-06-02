// Source: A. Costan, S. Gaubert, E. Goubault, M. Martel, S. Putot: "A Policy
// Iteration Algorithm for Computing Fixed Points in Static Analysis of
// Programs", CAV 2005

#include "assert.h"

/*@
  ensures \result == 0;
*/
int main() {
    int i,j;
    i = 1;
    j = 10;
    /*@
      loop invariant i + 2*j == 21;
      loop invariant i >= 1;
      loop invariant j <= 10;
      loop invariant i <= 21;
      loop invariant 0 <= j <= 10;
      loop invariant i <= j + 5;
      loop assigns i, j;
      loop variant j;
    */
    /* PROBE_HERE:loop1_before */
    while (j >= i) {
        /* PROBE_HERE:loop1_body_entry */
        i = i + 2;
        j = -1 + j;
    }
    //@ assert(j == 6);
    return 0;
}
