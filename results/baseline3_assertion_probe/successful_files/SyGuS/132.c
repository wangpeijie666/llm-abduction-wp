/*@ assigns \nothing; */
int unknown(void);

void foo(int j, int c, int t) {
    int i = 0;
    
    /*@
      loop invariant i >= 0;
      loop assigns i, j, t;
    */
    /* PROBE_HERE:loop1_before */
    while(unknown()) {
        /* PROBE_HERE:loop1_body_entry */
        if(c > 48) {
            if (c < 57) {
                j = i + i;
                t = c - 48;
                i = j + t;
            }
        }
    } 

    //post-condition
    //@ assert (i >= 0);
}
