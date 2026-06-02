/*@
  requires 0 <= x <= 10;
  requires 0 <= y <= 10;
*/
void foo(int x, int y) {
  // loop body
  /*@
    loop invariant 0 <= y ==> x >= 0;
    loop invariant y >= 0;
    loop invariant y > 0 ==> x + y <= \at(x,Pre) + \at(y,Pre) + 20*(y-\at(y,Pre))/10;
    loop invariant x - y == \at(x,Pre) - \at(y,Pre);
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x + 10;
    y  = y + 10;
  }
  // post-condition
  if (y == 0) {
    //@ assert(x != 20);
  }
}
