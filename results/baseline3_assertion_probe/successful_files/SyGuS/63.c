int main() {
    int x = 1;
    int y = 0;

    /*@
      loop invariant 1 <= x <= 11;
      loop invariant x <= 10 ==> (x == 1 ? y == 0 : y == 11 - x);
      loop invariant x == 11 ==> y == 0;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop1_before */
    while (x <= 10) {
        /* PROBE_HERE:loop1_body_entry */
        y = 10 - x;
        x = x +1;
    }

    //post-condition
    //@ assert (y >= 0);
    ////@ assert (y < 10);
}
