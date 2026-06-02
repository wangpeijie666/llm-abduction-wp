/*@
requires c>0;
assigns \nothing;

ensures a <= \old(m) || c > 0;
*/
void foo(int a, int m, int c) {
    int j = 0;
    int k = 0;

    /*@
      loop invariant 0 <= k <= c;
      loop invariant k == 0 || a <= m;
      loop assigns k, m;
    */
    /* PROBE_HERE:loop1_before */
    while ( k < c) {
        /* PROBE_HERE:loop1_body_entry */
        if(m < a) {
            m = a;
        }
        k = k + 1;
    }

    //post-condition
    if(c > 0) {
        //@ assert(a <=  m);
    }
}
