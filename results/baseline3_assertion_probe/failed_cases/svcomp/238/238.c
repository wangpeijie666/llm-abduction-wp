// Source: Isil Dillig, Thomas Dillig, Boyang Li, Ken McMillan: "Inductive
// Invariant Generation via Abductive Inference", OOPSLA 2013.

#include <limits.h>

/*@
    assigns \nothing;
    ensures \result >= INT_MIN && \result <= INT_MAX;
*/
int unknown_int();

/*@
    assigns \nothing;
*/
int main() {
    unsigned int i,j,a,b;
    int flag = unknown_int();
    a = 0;
    b = 0;
    j = 1;
    if (flag) {
        i = 0;
    } else {
        i = 1;
    }

    /*@
        loop invariant (j - i) == (flag ? 1u : 0u);
        loop invariant b == a * (j - i);
        // Bridge lemma for modular arithmetic simplification in WP:
        // from (j - i) == c, we also have c + (i + 2u) == (j + 2u) (mod 2^32)
        // which matches the i/j updates in the loop body and helps preserve the first invariant.
        loop invariant (flag ? 1u : 0u) + (i + 2u) == j + 2u;
        loop assigns a, b, i, j;
    */
    /* PROBE_HERE:loop1_before */
    while (unknown_int()) {
        /* PROBE_HERE:loop1_body_entry */
        a++;
        b += (j - i);
        i += 2;
        if (i%2 == 0) {
            j += 2;
        } else {
            j++;
        }
    }
    if (flag) {
        //@ assert(a == b);
    }
    return 0;
}
