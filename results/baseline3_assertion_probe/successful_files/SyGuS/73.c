/*@
requires y >= 127;
assigns \nothing;
*/
void foo(int y) {
  int c = 0;
  int z = 36 * y;

  /*@
    loop invariant c >= 0;
    loop invariant z == 36*y + c;
    loop assigns c, z;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    if (c < 36)
    {
      z = z + 1;
      c = c + 1;
    }
  }
  // post-condition
  if (z < 0) {
    if(z >= 4608) {
      //@ assert( (c >= 36) );
    }
  }
}
