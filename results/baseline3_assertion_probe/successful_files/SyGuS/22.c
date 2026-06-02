int unknown();

int main()
{
    int x = 1;
    int m = 1;
    int n;

    /*@
      loop invariant 1 <= x;
      loop invariant m >= 1;
      loop invariant m <= x;
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
    if(n > 1) {
       
       //@ assert (m >= 1);
    }
}
