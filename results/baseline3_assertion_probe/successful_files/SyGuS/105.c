/*@
requires n >= 0;
assigns \nothing;
ensures \true;
*/
void foo(int n) {
  int x = 0;
  
  /*@
    loop invariant 0 <= x <= n;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x < n) {
    /* PROBE_HERE:loop1_body_entry */
    x = x + 1;
  }
  // post-condition
  if (n >= 0) {
    //@ assert(x == n);
  }
}
