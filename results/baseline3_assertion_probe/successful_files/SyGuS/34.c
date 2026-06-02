/*@
requires n >= 0;
assigns \nothing;
ensures \true;
*/
void foo(int n) {
  int x = n;
  // loop body
  /*@
    loop invariant 0 <= x <= n;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 0) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
  }
  // post-condition
  if (n >= 0) {
    //@ assert(x == 0);
  }
}
