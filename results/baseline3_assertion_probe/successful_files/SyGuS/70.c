/*@
requires n > 0;
assigns \nothing;
*/
void foo(int n) {
    int x = 1;
    int y = 0;

    /*@
      loop invariant 1 <= x <= n + 1;
      loop invariant (x == 1 ==> y == 0) && (x > 1 ==> y == n - x + 1);
      loop invariant 0 <= y <= n;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop1_before */
    while (x <= n) {
        /* PROBE_HERE:loop1_body_entry */
        y = n - x;
        x = x +1;
    }

    //post-condition
    if (n > 0) {
      //@ assert (y >= 0);
      //@ assert (y < n);
    }
}
