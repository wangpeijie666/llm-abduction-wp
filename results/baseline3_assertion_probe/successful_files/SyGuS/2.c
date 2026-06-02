void main() {
  // variable declarations
  int x;
  int y;
  // pre-conditions
  x = 1;
  y = 0;
  // loop body
  /*@
    loop invariant 0 <= y <= 1000;
    loop invariant x >= y;
    loop invariant x >= 1;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (y < 1000) {
    /* PROBE_HERE:loop1_body_entry */
    x  = (x + y);
    y  = (y + 1);
  }
  // post-condition
  //@ assert(x >= y);
}
