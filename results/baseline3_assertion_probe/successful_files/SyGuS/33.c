/*@
requires n < 0;
assigns \nothing;
ensures n < 0;
*/
void foo(int n) {
  int x = n;
  // loop body
  /*@
    loop invariant x == n;
    loop invariant n < 0;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 0) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
  }
  // post-condition
  if (x != 0) {
    //@ assert(n < 0);
  }
}
