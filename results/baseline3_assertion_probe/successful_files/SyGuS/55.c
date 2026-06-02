/*@
requires n > 0;
assigns \nothing;
*/
void foo(int n) {
  int c = 0;
  
  /*@
    loop invariant 0 <= c <= n || c > n;
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
  if (c < 0) {
    if (c > n) {
      //@ assert(c == n);
    }
  }
}
