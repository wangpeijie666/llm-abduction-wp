int main() {
  int i = 1;
  int sn = 0;
  
  /*@
    loop invariant 1 <= i <= 9;
    loop invariant sn == i - 1;
    loop assigns i, sn;
  */
  /* PROBE_HERE:loop1_before */
  while (i <= 8) {
    /* PROBE_HERE:loop1_body_entry */
    i  = i + 1;
    sn  = sn + 1;
  }
  // post-condition
  if (sn != 0) {
    //@ assert(sn == 8);
  }
}
