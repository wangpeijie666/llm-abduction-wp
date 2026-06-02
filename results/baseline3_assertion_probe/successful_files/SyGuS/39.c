int unknown();

/*@
  assigns \nothing;
*/
int unknown();

/*@
requires n > 0;
assigns \nothing;
*/
void foo(int n) {
    int c = 0;

    /*@
      loop invariant n > 0;
      loop invariant c >= 0;
      loop assigns c;
    */
    /* PROBE_HERE:loop1_before */
    while (unknown()) {
        /* PROBE_HERE:loop1_body_entry */
        if(c == n) {
            c = 1;
        }
        else {
            c = c + 1;
        }
    }

    //post-condition
    if(c == n) {
        //@ assert( c >= 0);
        //@ assert( c <= n);
    }
}
