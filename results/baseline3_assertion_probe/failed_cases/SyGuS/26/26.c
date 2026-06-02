/*@
requires x == n;
requires x != 1;
assigns \nothing;
ensures \true;
*/
void foo(int x, int n) {
  // loop body
  /*@
    loop invariant \true;
    loop invariant \true;
    loop invariant x <= 1 ==> x == n;
    loop assigns x;
    loop variant x;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 1) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
  }
  // post-condition
  if (x != 1) {
    //@ assert(n < 1);
  }
}
