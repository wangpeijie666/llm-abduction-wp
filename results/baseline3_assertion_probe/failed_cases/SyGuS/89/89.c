/*@
requires x == y;
assigns \nothing;
*/
void foo(int x, int y) {
  int lock = 1;
  
  /*@
    loop invariant x == y;
    loop invariant lock == 0 || lock == 1;
    loop assigns x, y, lock;
  */
  /* PROBE_HERE:loop1_before */
  while (x != y) {  
    /* PROBE_HERE:loop1_body_entry */
    if (unknown()) {
      lock = 1;
      x = y;
    } else {
      lock  = 0;
      x  = y;
      y  = y + 1; 
    }
  }
  // post-condition
  //@ assert(lock == 1);
}
