/*@
requires x >= 0;
requires y >= 0;
requires x >= y;
assigns \nothing;
*/
void foo(int x, int y) {
  int i = 0;
  
  /*@
    loop invariant i >= 0;
    loop invariant i <= y;
    loop assigns i;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    if (i < y)
    {
      i = i + 1;
    }
  }
  // post-condition
  if (i >= x) {
    if (0 > i) {
      //@ assert(i >= y);
    }
  }
}
