/*@
requires n > 0;
assigns \nothing;
*/
void foo(int n) {
  int c = 0;

  /*@
    loop invariant n > 0;
    loop invariant c <= n;
    loop assigns c;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    if (unknown()) {
      if (c > n) {
        c = c + 1;
      }
    } else {
      if (c == n) {
        c = 1;
      }
    }
  }
  // post-condition
  if (c != n) {
    //@ assert(c <= n);
  }
}
