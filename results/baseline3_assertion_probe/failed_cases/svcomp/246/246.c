#include <limits.h>
/*@
    ensures \result >= INT_MIN && \result <= INT_MAX;
    assigns \nothing;
*/
int unknown_int();

int main() {
    int i, j, k, n;

    k = unknown_int();
    n = unknown_int();
    if (k == n) {
    }
    else {
        goto END;
    }

    /*@
        loop invariant 0 <= i <= n;
        loop assigns i, j, k;
        loop invariant k == n;
    */
    /* PROBE_HERE:loop1_before */
    for (i = 0; i < n; i++) {
        /* PROBE_HERE:loop1_body_entry */
        /*@
            loop invariant 2 * i <= j <= n;
            loop assigns j, k;
            loop invariant k == n;
        */
        /* PROBE_HERE:loop2_before */
        for (j = 2 * i; j < n; j++) {
            /* PROBE_HERE:loop2_body_entry */
            if (unknown_int()) {
                /*@
                    loop invariant j <= k <= n;
                    loop assigns k;
                */
                /* PROBE_HERE:loop3_before */
                for (k = j; k < n; k++) {
                    /* PROBE_HERE:loop3_body_entry */
                    //@ assert(k >= 2 * i);
                }
            } else {
                //@ assert(k >= n);
                //@ assert(k <= n);
            }
        }
    }
END:
    return 0;
}
