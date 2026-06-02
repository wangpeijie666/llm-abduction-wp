void foo(int n) {
  int x = 0;

  /*@
    loop invariant 0 <= x;
    loop invariant 0 <= n ==> x <= n;
    loop invariant x < n ==> n >= 0;
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
