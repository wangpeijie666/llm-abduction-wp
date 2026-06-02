/*@
requires n >= 0;
requires k >= 0;
*/
void foo(int k, int n) {
  int i = 0;
  int j = 0;
  
  /*@
    loop invariant 0 <= i <= n+1;
    loop invariant j >= 0;
    loop invariant j >= i;
    loop assigns i, j;
  */
  /* PROBE_HERE:loop1_before */
  while (i <= n) {
    /* PROBE_HERE:loop1_body_entry */
    i  = i + 1;
    j  = j + i;
  }
  // post-condition
  //@ assert(i + j + k > 2*n);
}
