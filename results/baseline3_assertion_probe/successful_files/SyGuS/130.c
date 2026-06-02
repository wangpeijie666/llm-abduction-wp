/*@ requires x2 >= 0; */
void foo(int x2, int x3) {
    int d1 = 1;
    int d2 = 1;
    int d3 = 1;
    int x1 = 1;

    /*@
      loop invariant 0 <= x1 <= 1;
      loop invariant x2 >= 0;
      loop invariant \true;
      loop assigns x1, x2, x3;
    */
    /* PROBE_HERE:loop1_before */
    while(x1 > 0) {
        /* PROBE_HERE:loop1_body_entry */
        if(x2 > 0) {
            if(x3 > 0) {
                x1 = x1 - d1;
                x2 = x2 - d2;
                x3 = x3 - d3;
            }
        }
    }

    //@ assert (x2 >= 0);
    ////@ assert (x3 >= 0);
}
