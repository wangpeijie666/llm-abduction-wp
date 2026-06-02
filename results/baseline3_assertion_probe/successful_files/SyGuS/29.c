/*@
requires x == n;
requires n >= 0;
assigns \nothing;
ensures x == \old(x);
ensures n == \old(n);
*/
void foo(int x, int n) { 
  // loop body
  /*@
    loop invariant 0 <= x <= n;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 0) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
  }
  // post-condition
  if (n >= 0) {
    //@ assert(x == 0);
  }
}
