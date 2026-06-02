/*@
requires size >= 1;
assigns \nothing;
*/
void foo(int size) {
  int i = 1;
  int sn = 0;
  
  /*@
    loop invariant 1 <= i <= size + 1;
    loop invariant sn == i - 1;
    loop assigns i, sn;
  */
  /* PROBE_HERE:loop1_before */
  while (i <= size) {
    /* PROBE_HERE:loop1_body_entry */
    i = i + 1;
    sn = sn + 1;
  }
  // post-condition
  if(sn != size) {
    //@ assert(sn == 0);
  }
}
