int main() {
  int x = 0;
  
  /*@
    loop invariant 0 <= x <= 100;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while (x < 100) {
    /* PROBE_HERE:loop1_body_entry */
    x = x + 1;
  }
  // post-condition
  //@ assert(x == 100);
}
