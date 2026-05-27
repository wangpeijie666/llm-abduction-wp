// sum01_true-unreach-call_true-termination.c

/*@
    requires \true;
    ensures \result == 0;
*/
int main() {
    int n;
    int i = 0;
    int sn = 0;

    /*@
        loop invariant 1 <= i <= n + 1;
        loop invariant sn == 2 * (i - 1);
        loop assigns i, sn;
        loop variant n - i + 1;
    */
    /* PROBE_HERE:loop1_before */
    for (i = 1; i <= n; i++) {
        /* PROBE_HERE:loop1_body_entry */
        sn = sn + (2);
    }

    //@ assert(sn == n * (2) || sn == 0);

    return 0;
}
