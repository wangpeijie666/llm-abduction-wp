int fun(int x, int y) {
    int r = x;
    int d = 0;

    /*@
      loop invariant r + d*y == x;
      loop assigns r, d;
    */
    /* PROBE_HERE:loop1_before */
    while (r >= y) {
        /* PROBE_HERE:loop1_body_entry */
        // Beginning
        r = r - y;
        d = d + 1;
        // ENd
        //@ assert r + d*y == x;
    }
    return d;
}
