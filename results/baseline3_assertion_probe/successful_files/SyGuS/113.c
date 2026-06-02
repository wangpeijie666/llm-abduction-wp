/*@
requires 1 <= n;
assigns \nothing;
*/
void foo(int n) {
  int i = 1;
  int sn = 0;
  
  /*@
    loop invariant 1 <= i <= n+1;
    loop invariant sn == i-1;
    loop assigns i, sn;
  */
  /* PROBE_HERE:loop1_before */
  while (i <= n) {
    /* PROBE_HERE:loop1_body_entry */
    i = i + 1;
    sn = sn + 1;
  }
  // post-condition
  if (sn != 0) {
    //@ assert(sn == n);
  }
}
