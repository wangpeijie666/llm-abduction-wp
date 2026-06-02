/*@ 
  requires 0 <= x <= 2;
  requires 0 <= y <= 2;
*/
void foo(int x, int y) {
  // loop body
  /*@
    loop invariant 0 <= x;
    loop invariant 0 <= y;
    loop invariant (x - y) == 0 || (x - y) == -1 || (x - y) == -2 || (x - y) == 1 || (x - y) == 2;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x + 2;
    y  = y + 2;
  }
  // post-condition
  if (y == 0) {
    //@ assert(x != 4);
  }
}
