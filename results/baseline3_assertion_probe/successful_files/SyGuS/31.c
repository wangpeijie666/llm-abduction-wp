/*@
requires n < 0;
assigns \nothing;
*/
void foo(int n) {
  int x = n;
  // loop body
  /*@
    loop invariant x == n;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 1) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
  }
  // post-condition
  if (x != 1) {
    //@ assert(n < 0);
  }
}
