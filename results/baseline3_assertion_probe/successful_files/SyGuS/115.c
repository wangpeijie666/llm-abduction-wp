int unknown();

/*@
  assigns \nothing;
*/
int main() {
  int sn = 0;
  int x = 0;
  
  /*@
    loop invariant sn == x;
    loop assigns sn, x;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x + 1;
    sn  = sn + 1;
  }
  // post-condition
  if (sn != -1) {
    //@ assert(sn == x);
  }
}
