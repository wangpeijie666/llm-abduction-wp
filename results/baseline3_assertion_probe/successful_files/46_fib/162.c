int unknown1();
int unknown2();
int unknown3();

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();
/*@ assigns \nothing; */
int unknown3();

void main() {
  int a = 1;
  int b = 1;
  int c = 2;
  int d = 2;
  int x = 3;
  int y = 3;
  /*@
    loop invariant a + c == b + d;
    loop assigns a, b, c, d, x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown1()) {
    /* PROBE_HERE:loop1_body_entry */
    x = a + c;
    y = b + d;
    if ((x + y) % 2 == 0) {
      a++;
      d++;
    } else {
      a--;
    }

    /*@
      loop invariant a + c == b + d;
      loop assigns c, b;
    */
    /* PROBE_HERE:loop2_before */
    while (unknown2()) {
      /* PROBE_HERE:loop2_body_entry */
      c--;
      b--;
    }
  }
  //@ assert(a + c == b + d);
}
