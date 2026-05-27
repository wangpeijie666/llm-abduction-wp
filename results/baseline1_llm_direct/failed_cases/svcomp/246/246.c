#include <limits.h>
/*@
    ensures \result >= INT_MIN && \result <= INT_MAX;
*/
int unknown_int();

int main() {
    int i, j, k, n;

    k = unknown_int();
    n = unknown_int();
    if (k == n) {
        // No operation, but condition is valid.
    } else {
        goto END;
    }

    /*@
        loop invariant 0 <= i;
        loop invariant i <= n;
        loop assigns i, j, k;
    */
    for (i = 0; i < n; i++) {
        /*@
            loop invariant 2 * i <= j;
            loop invariant j <= n;
            loop invariant 0 <= i && i < n;
            loop assigns j, k;
        */
        for (j = 2 * i; j < n; j++) {
            if (unknown_int()) {
                /*@
                    loop invariant j <= k;
                    loop invariant k <= n;
                    loop invariant 2 * i <= k;
                    loop assigns k;
                */
                for (k = j; k < n; k++) {
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
