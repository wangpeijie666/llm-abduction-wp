void foo(int n) {
  int x = 0;
  
  /*@
    loop invariant 0 <= x;
    loop invariant x <= n || n < 0;
    loop invariant n >= 0 ==> x <= n;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x < n) {
    /* PROBE_HERE:loop1_body_entry */
    x = x + 1;
  }
  // post-condition
  if (x != n) {
    //@ assert(n < 0);
  }
}
