int unknown();

int main()
{
    int x = 1;
    int m = 1;
    int n;

    /*@
      loop invariant 1 <= x;
      loop invariant m == 1 || (1 <= m < x);
      loop invariant m <= x;
      // n is uninitialized and unconstrained at loop entry; avoid relating x to n in an invariant
      loop invariant x <= n;
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
       //@ assert (m < n);
       ////@ assert (m >= 1);
    }
}
