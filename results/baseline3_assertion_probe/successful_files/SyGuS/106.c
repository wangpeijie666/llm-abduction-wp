/*@
requires a <= m;
requires j < 1;
assigns \nothing;
*/
void foo(int a, int j, int m) {
    int k = 0;

    /*@
      loop invariant 0 <= k <= 1;
      loop invariant a <= m;
      loop assigns k, m;
    */
    /* PROBE_HERE:loop1_before */
    while (k < 1) {
        /* PROBE_HERE:loop1_body_entry */
        if(m < a) {
            m = a;
        }
        k = k + 1;
    }
    //post-condition
    //@ assert(a <= m);
}
