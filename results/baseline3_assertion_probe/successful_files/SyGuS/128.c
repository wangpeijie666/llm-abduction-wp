void foo(int y) {
  int x = 1;
  
  /*@
    loop invariant x >= 1;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x < y) {
    /* PROBE_HERE:loop1_body_entry */
    x = x + x;
  }
  // post-condition
  //@ assert(x >= 1);
}
