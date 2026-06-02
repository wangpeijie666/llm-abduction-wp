/*@
requires x == n;
requires x != 0;
assigns \nothing;
ensures x == \old(x);
ensures n == \old(n);
*/
void foo(int x, int n) { 
  // loop body
  /*@
    loop invariant n == \at(n,LoopEntry);
    loop invariant x == \at(x,LoopEntry) - (\at(x,LoopEntry) - x);
    loop invariant (\at(x,LoopEntry) == n) ==> (n <= 0 || (0 <= x <= n));
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x > 0) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x - 1;
  }
  // post-condition
  if (x != 0) {
    //@ assert(n < 0);
  }
}
