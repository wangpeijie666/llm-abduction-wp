void foo(int x, int y) {
  int i = x;
  int j = y;
  
  /*@
    loop invariant x <= i;
    loop invariant y <= j;
    loop invariant y - x == j - i;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (x != 0) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
    y  = y - 1;
  }
  
  // post-condition
  if(i == j) {
    //@ assert(y == 0);
  }
}
