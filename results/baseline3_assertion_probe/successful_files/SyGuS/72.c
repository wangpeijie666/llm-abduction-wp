/*@ 
  requires y <= 127;
  assigns \nothing;
*/
void foo(int y) {
  int c = 0;
  int z = 36 * y;
  
  /*@
    loop invariant 0 <= c <= 36;
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
  if(c < 36) {
    //@ assert(z < 4608);
  }
}
