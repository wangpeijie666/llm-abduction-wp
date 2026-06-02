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
      loop invariant j >= i ==> (i + j == 11);
      loop invariant j < i ==> (j == 6 && i == 11);
      loop assigns i, j;
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
