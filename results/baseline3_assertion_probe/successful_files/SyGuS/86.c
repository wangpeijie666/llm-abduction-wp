int main() {
  int x = -50;
  int y = 0;
  
  /*@
    loop invariant 2*(x+50) == y*(y-1);
    loop invariant (y+1)*(y+2) == (y*(y+1)) + (2*y + 2);
    loop invariant x < 0 ==> y <= 10;
    loop invariant y >= 0;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (x < 0) {
    /* PROBE_HERE:loop1_body_entry */
    x  = x + y;
    y  = y + 1;
  }
  // post-condition
  //@ assert(y > 0);
}
