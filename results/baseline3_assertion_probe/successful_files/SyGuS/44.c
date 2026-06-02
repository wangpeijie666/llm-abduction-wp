int unknown();

/*@ 
  assigns \nothing;
*/
int unknown();

/*@
requires n > 0;
assigns \nothing;
*/
void foo(int n) {
  int c = 0;

  /*@
    loop assigns c;
    loop invariant n > 0;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    if (unknown()) {
      if (c > n) {
        c = c + 1;
      }
    } else {
      if (c == n) {
        c = 1;
      }
    }
  }
  // post-condition
  if (n <= -1) {
    //@ assert(c != n);
  }
}
