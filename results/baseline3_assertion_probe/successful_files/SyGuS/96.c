void foo(int x) {
  int i = 0;
  int j = 0;
  int y = 0;
  
  /*@
    loop invariant 0 <= i;
    loop invariant j == 0;
    loop assigns i, j;
  */
  /* PROBE_HERE:loop1_before */
  while (i <= x) {
    /* PROBE_HERE:loop1_body_entry */
    i  = i + 1;
    j  = j + y;
  }
  // post-condition
  if (i != j) {
    //@ assert(y != 1);
  }
}
