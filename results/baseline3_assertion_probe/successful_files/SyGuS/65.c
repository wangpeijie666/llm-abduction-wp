int main() {
    int x = 1;
    int y = 0;

    /*@
      loop invariant 1 <= x <= 102;
      loop invariant 0 <= y;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop1_before */
    while (x <= 100) {
        /* PROBE_HERE:loop1_body_entry */
        y = 100 - x;
        x = x +1;
    }

    //post-condition
    //@ assert (y >= 0);
    ////@ assert (y < 100);
}
