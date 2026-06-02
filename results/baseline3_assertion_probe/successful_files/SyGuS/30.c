/*@
requires (x == 100);
assigns \nothing;
ensures x == \old(x);
*/
void foo(int x) { 
  // loop body
  /*@
    loop invariant 0 <= x <= 100;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 0) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
  }
  // post-condition
  //@ assert(x == 0);
}
