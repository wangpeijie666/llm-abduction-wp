#include <limits.h>

/*@
    ensures 0 <= \result <= INT_MAX;
    assigns \nothing;
*/
int unknown_int();

int main() {
    int n;
    int k = 0;
    int i = 0;

    n = unknown_int();

    /*@
        loop invariant 0 <= i && i <= n;
        loop invariant k == i;
        loop assigns i, k;
    */
    /* PROBE_HERE:loop1_before */
    while (i < n) {
        /* PROBE_HERE:loop1_body_entry */
        i++;
        k++;
    }

    int j = n;

    /*@
        loop invariant 0 <= j <= n;
        loop invariant k == j;
        loop assigns j, k;
    */
    /* PROBE_HERE:loop2_before */
    while (j > 0) {
        /* PROBE_HERE:loop2_body_entry */
        //@ assert(k > 0);
        j--;
        k--;
    }

    return 0;
}
