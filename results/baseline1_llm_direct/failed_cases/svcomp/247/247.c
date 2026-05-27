#include <limits.h>
/*@
    ensures \result >= INT_MIN && \result <= INT_MAX;
*/
int unknown_int();

int __BLAST_NONDET;

int main() {
    int i, j, k, n, l, m;

    n = unknown_int();
    m = unknown_int();
    l = unknown_int();

    //@ assert n >= INT_MIN && n <= INT_MAX;
    //@ assert m >= INT_MIN && m <= INT_MAX;
    //@ assert l >= INT_MIN && l <= INT_MAX;

    if (3 * n <= m + l); else goto END;

    /*@
        loop invariant 0 <= i <= n;
        loop assigns i, j, k;
    */
    for (i = 0; i < n; i++)
        /*@
            loop invariant 2 * i <= j <= 3 * i;
            loop invariant 0 <= i <= n;
            loop assigns j, k;
        */
        for (j = 2 * i; j < 3 * i; j++)
            /*@
                loop invariant i <= k < j;
                loop invariant 0 <= i <= n;
                loop assigns k;
            */
            for (k = i; k < j; k++)
                //@ assert k - i <= 2 * n;
END:
    return 0;
}
