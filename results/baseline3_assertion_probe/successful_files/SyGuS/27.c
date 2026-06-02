/*@
requires x == n;
requires n >= 1;
assigns \nothing;
ensures \true;
*/
void foo(int x, int n) {
  // loop body
  /*@
    loop invariant 1 <= x <= n;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 1) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
  }
  // post-condition
  if (n >= 0) {
    //@ assert(x == 1);
  }
}
