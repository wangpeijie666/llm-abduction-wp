void foo(int x, int y) {
  int i = x;
  int j = y;
  
  /*@
    loop invariant x <= i;
    loop invariant y == j + (x - i);
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (x != 0) {
    /* PROBE_HERE:loop1_body_entry */
    x = x - 1;
    y = y - 1;
  }
  // post-condition
  if(y != 0) {
    //@ assert(i != j);
  }
}
