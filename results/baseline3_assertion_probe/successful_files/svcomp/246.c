#include <limits.h>
/*@
    assigns \nothing;
    ensures \result >= INT_MIN && \result <= INT_MAX;
*/
int unknown_int();

/*@
    ensures \result == 0;
*/
int main() {
    int i,j,k,n;

    k = unknown_int();
    n = unknown_int();
    if( k == n) {
    }
    else {
        goto END;
    }

    /*@
        loop invariant 0 <= i;
        loop invariant i <= (n > 0 ? n : 0);
        loop invariant k == n;
        loop assigns i, j, k;
    */
    /* PROBE_HERE:loop1_before */
    for (i = 0; i < n; i++) {
        /* PROBE_HERE:loop1_body_entry */
        /*@
            loop invariant 0 <= i;
            // j is only initialized at entry of the inner loop; do not require bounds that may fail when j=2*i.
            loop invariant k == n;
            loop invariant 2*i <= j;
            loop assigns j, k;
        */
        /* PROBE_HERE:loop2_before */
        for (j= 2 * i; j < n; j++) {
            /* PROBE_HERE:loop2_body_entry */
            if( unknown_int()) {
                /*@
                    loop invariant j <= k <= n;
                    loop invariant 2*i <= j;
                    loop invariant k >= 2*i;
                    loop assigns k;
                */
                /* PROBE_HERE:loop3_before */
                for (k = j; k < n; k++) {
                    /* PROBE_HERE:loop3_body_entry */
                    //@ assert(k >= 2*i);
                }
                /*@ assert k == n; */
            }
            else {
                //@ assert( k >= n );
                //@ assert( k <= n );
            }
        }
    }
END:
    return 0;
}
