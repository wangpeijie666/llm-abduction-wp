/*@
requires a <= m;
assigns \nothing;
ensures a <= m;
*/
void foo(int a, int m, int c) {
    int j = 0;
    int k = 0;

    /*@
      loop invariant 0 <= k;
      loop invariant a <= m;
      loop assigns k, m;
    */
    /* PROBE_HERE:loop1_before */
    while (k < c) {
        /* PROBE_HERE:loop1_body_entry */
        if(m < a) {
            m = a;
        }
        k = k + 1;
    }

    //post-condition
    //@ assert(a <= m);
}
