/*@
    requires x == 1 && y == 2;
    requires \valid(r);
    requires *r == 3;
    assigns *r;
*/
int fun(int x, int y , int *r) {
    *r = x;
    int d = 0;

    /*@
        loop invariant \valid(r);
        loop invariant y == 2;
        loop invariant x == 1;
        loop invariant *r + d * y == x;
        loop invariant d >= 0;
        loop invariant *r >= 0;
        loop assigns *r, d;
    */
    /* PROBE_HERE:loop1_before */
    while (*r >= y) {
        /* PROBE_HERE:loop1_body_entry */
        *r = *r - y;
        d = d + 1;
    }
    //@ assert *r == 1;
    //@ assert d == 0;
}
