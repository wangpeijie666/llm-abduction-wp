#include <limits.h>
/*@
    ensures \result >= INT_MIN && \result <= INT_MAX;
    assigns \nothing;
*/
int unknown_int();


int __BLAST_NONDET;

/*@
    ensures \result == 0;
*/
int main() {
    int i,j,k,n,l,m;

    n = unknown_int();
    m = unknown_int();
    l = unknown_int();
    if(3*n<=m+l); else goto END;
    /*@
      loop invariant 0 <= i;
      loop assigns i, j, k;
    */
    /* PROBE_HERE:loop1_before */
    for (i=0;i<n;i++)
        /*@
          loop invariant 0 <= i <= n;
          loop invariant 2*i <= j <= 3*i;
          loop assigns j, k;
        */
        /* PROBE_HERE:loop2_before */
        for (j = 2*i;j<3*i;j++)
            /*@
              loop invariant 0 <= i <= n;
              loop invariant 2*i <= j <= 3*i;
              loop invariant i <= k <= j;
              loop invariant k - i <= 2*n;
              loop assigns k;
            */
            /* PROBE_HERE:loop3_before */
            for (k = i; k< j; k++)
                //@ assert( k-i <= 2*n );
END:
    return 0;
}
