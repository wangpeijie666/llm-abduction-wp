// Source: E. De Angelis, F. Fioravanti, J. A. Navas, M. Proietti:
// "Verification of Programs by Combining Iterated Specialization with
// Interpolation", HCVS 2014

#include "assert.h"

/*@
  ensures \result == 0;
*/
int main() {
    int x = 1;
    int y = 0;
    /*@
      loop invariant 0 <= y <= 1000;
      loop invariant x >= 1 + (y*(y-1))/2;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop1_before */
    while (y < 1000) {
        /* PROBE_HERE:loop1_body_entry */
        x = x + y;
        y = y + 1;
    }
    //@ assert(x >= y);
    return 0;
}
