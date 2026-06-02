/*@
requires x >= 0;
requires y >= 0;
requires x >= y;
assigns \nothing;
*/
void foo(int x, int y) {
  int i = 0;

  /*@
    loop invariant 0 <= i;
    loop invariant i <= y;
    loop assigns i;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    if ( (i < y) )
    {
    (i  = (i + 1));
    }
  }
  // post-condition
  if (i < y) {
    //@ assert(0 <= i);
  }
}
