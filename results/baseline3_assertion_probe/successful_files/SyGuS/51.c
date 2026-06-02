/*@ assigns \nothing; */
int unknown(void);

void main() {
  int c = 0;
  
  /*@
    loop invariant c <= 4;
    loop assigns c;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown()) {
      /* PROBE_HERE:loop1_body_entry */
      if (unknown()) {
        if (c != 4) {
          c = c + 1;
        }
      } else {
        if (c == 4) {
          c = 1;
        }
      }
  }
  // post-condition
  if (c != 4){
    //@ assert(c <= 4);
  }
}
