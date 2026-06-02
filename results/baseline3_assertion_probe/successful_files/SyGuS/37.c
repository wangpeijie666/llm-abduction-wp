int unknown();

/*@
  assigns \nothing;
*/
int main() {
  int c = 0;

  /*@
    loop invariant 0 <= c <= 40;
    loop assigns c;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
    /* PROBE_HERE:loop1_body_entry */
    if (unknown()) {
      if (c != 40) {
        c  = c + 1;
      }
    } else {
      if (c == 40) {
        c  = 1;
      }
    }
  }
  // post-condition
  if (c < 0) {
    if (c > 40) {
      //@ assert( (c == 40) );
    }
  }
}
