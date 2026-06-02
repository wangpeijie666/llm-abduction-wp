int main() {
  int x = -5000;
  int y = 0;
  
  /*@
    loop invariant x == -5000 + (y*(y-1))/2;
    loop invariant y >= 0;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while ((x < 0)) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x + y;
    y  = y + 1;
  }
  // post-condition
  //@ assert(y > 0);
}
