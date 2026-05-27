// bhmr2007_true-unreach-call.c
// Source: Dirk Beyer, Thomas A. Henzinger, Rupak Majumdar, Andrey
// Rybalchenko: "Path Invariants", PLDI 2007.
#include <limits.h>

/*@
  ensures INT_MIN <= \result <= INT_MAX;
*/
int unknown_int();

int main() {
    int i, n, a, b;
    i = 0; a = 0; b = 0;
    
    /*@
      loop invariant 0 <= i;
      loop invariant 0 <= a && 0 <= b;
      loop invariant a + b == 3 * i;
      loop invariant i <= n;
      loop assigns i, a, b;
    */
    while (i < n) {
        int boolean;
        if (boolean != 0) {
            a = a + 1;
            b = b + 2;
        } else {
            a = a + 2;
            b = b + 1;
        }
        i = i + 1;
    }

    //@ assert(a + b == 3 * n);
    
    return 0;
}
