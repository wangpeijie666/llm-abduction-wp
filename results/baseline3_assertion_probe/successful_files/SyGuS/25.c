/*@
  requires x == 10000;
  assigns \nothing;
*/
void foo(int x) {
  /*@
    loop invariant 0 <= x <= 10000;
    loop invariant x == 10000 - (10000 - x);
    loop assigns x;
  */
  // loop body
  /* PROBE_HERE:loop1_before */
  while ((x > 0)) {
    /* PROBE_HERE:loop1_body_entry */
    (x  = (x - 1));
  }
  // post-condition
  //@ assert( (x == 0) );
}
