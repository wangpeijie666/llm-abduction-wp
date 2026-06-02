/*@
requires n >= 0;
assigns \nothing;
*/
void foo(int n) {
  int i = 0;
  int x = 0;
  int y = 0;
    
  /*@
    loop invariant 0 <= i <= n;
    loop invariant x >= 0 && y >= 0;
    loop invariant x + y == 3*i;
    loop assigns i, x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (i < n) {
    /* PROBE_HERE:loop1_body_entry */
    i = i + 1;
    if (unknown()) {
      x  = x + 1;
      y  = y + 2;
    } else {
      x  = x + 2;
      y  = y + 1;
    }
  }
  // post-condition
  //@ assert((3 * n) == (x + y));
}
