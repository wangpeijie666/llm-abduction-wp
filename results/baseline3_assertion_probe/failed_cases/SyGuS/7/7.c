/*@
  requires 0 <= x <= 10;
  requires 0 <= y <= 10;
  assigns \nothing;
*/
int unknown(void);

/*@
  requires 0 <= x <= 10;
  requires 0 <= y <= 10;
  assigns x, y;
*/
void foo(int x, int y) {
  // loop body
  /*@
    loop invariant y == \at(y,Pre) + (x - \at(x,Pre));
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
