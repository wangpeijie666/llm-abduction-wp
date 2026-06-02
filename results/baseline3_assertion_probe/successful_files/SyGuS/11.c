/*@
  requires 0 <= x <= 10;
  requires 0 <= y <= 10;

*/
void foo(int x, int y) {
  // loop body
  /*@
    loop invariant x >= 0;
    loop invariant y >= 0;
    loop invariant x % 10 == x - 10 * (x / 10);
    loop invariant y % 10 == y - 10 * (y / 10);
    loop invariant (x == 20) ==> (y != 0);
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x + 10;
    y  = y + 10;
  }
  // post-condition
  if (x == 20) {
    //@ assert(y != 0);
  }
}
