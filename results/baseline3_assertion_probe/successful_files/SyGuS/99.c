/*@
requires n >= 0;
assigns \nothing;
ensures \true;
*/
void foo(int n) {
  int x = n;
  int y = 0;
  
  /*@
    loop invariant 0 <= x <= n;
    loop invariant 0 <= y <= n;
    loop invariant x + y == n;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 0) {
    /* PROBE_HERE:loop1_body_entry */
    y  = y + 1;
    x  = x - 1;
  }
  // post-condition
  //@ assert(n == x + y);
}
