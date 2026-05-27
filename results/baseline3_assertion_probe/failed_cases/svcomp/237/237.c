#include <limits.h>
/*@
    ensures 0 <= \result <= 1;
    assigns \nothing;
*/
int unknown_int();

int main() {
    int i, j, k;
    i = 1;
    j = 1;
    k = unknown_int();
    /*@
        loop invariant 1 <= i <= INT_MAX;
        loop invariant j == i + k;
        loop invariant k <= 1;
        loop invariant k >= 0;
        loop invariant 1 <= i + k <= 2;
        loop invariant k == 0 ==> j == i;
        loop assigns i, j, k;
    */
    /* PROBE_HERE:loop1_before */
    while (i < INT_MAX) {
        /* PROBE_HERE:loop1_body_entry */
        i = i + 1;
        j = j + k;
        k = k - 1;
        //@ assert(1 <= i + k && i + k <= 2 && i >= 1);
    }
    return 0;
}
