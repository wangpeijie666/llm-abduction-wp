/*@
requires i == 1;
requires j == 10;
assigns i, j;
ensures j < i;
*/
void foo(int i, int j) {
  // loop body
  /*@
    loop invariant j - i == 9 - 3 * \at(i,Pre) + 3 * i; 
    loop invariant i + 2*j == 21;
    loop invariant j >= 0;
    loop assigns i, j;
  */
  /* PROBE_HERE:loop1_before */
  while (j >= i) {
    /* PROBE_HERE:loop1_body_entry */
    i  = i + 2;
    j  = j - 1;
  }
  // post-condition
  //@ assert(j == 6);
}
