/*@
  requires 0 <= x <= 10;
  requires 0 <= y <= 10;
  assigns \nothing;
*/
int unknown(void);

/*@
  requires 0 <= x <= 10;
  requires 0 <= y <= 10;
  assigns \nothing;
*/
void foo(int x, int y) {
  // variable declarations
  int z1;
  int z2;
  int z3;

  // loop body
  /*@
    loop invariant 0 <= x;
    loop invariant 0 <= y;
    loop invariant x == \at(x,Pre) + 10 * kx;
    loop invariant y == \at(y,Pre) + 10 * ky;
    loop invariant kx >= 0;
    loop invariant ky >= 0;
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
