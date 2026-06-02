/*@
requires i == 1;
requires j == 20;
assigns i, j;
ensures j == 13;
*/
void foo(int i, int j) {
  // loop body
  /*@
    loop invariant j - i == 19 - 3*(i-1)/2;
    loop invariant i % 2 == 1;
    loop assigns i, j;
  */
  /* PROBE_HERE:loop1_before */
  while (j >= i) {
    /* PROBE_HERE:loop1_body_entry */
    i  = i + 2;
    j  = j - 1;
  }
  // post-condition
  //@ assert(j == 13);
}
