/*@
requires n > 0;
assigns \nothing;
*/
void foo(int n)
{
    int x = 0;
    int m = 0;

    /*@ 
      loop invariant 0 <= x <= n;
      loop invariant 0 <= m;
      loop invariant m < n;
      loop assigns x, m;
    */
    /* PROBE_HERE:loop1_before */
    while (x < n) {
        /* PROBE_HERE:loop1_body_entry */
        if (unknown()) {
            m = x;
        }
        x = x + 1;
    }

    //post-condition
    if(n > 0) {
       //@ assert (m < n);
       //@ assert (m >= 0);
    }
}
