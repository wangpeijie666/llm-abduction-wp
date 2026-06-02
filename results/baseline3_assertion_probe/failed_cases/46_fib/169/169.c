int unknown1();
int unknown2();
int unknown3();

/*@
  assigns \nothing;
*/
void foo(int flag) {
  int a = 0;
  int b = 0;
  int x = 0;
  int y = 0;
  int z = 0;
  int j = 0;
  int w = 0;

  /*@
    loop invariant a == b;
    loop invariant 0 <= z;
    loop invariant -1 <= z;
    loop invariant -2 <= z;
    loop invariant w >= z;
    loop assigns a, b, x, y, z, j, w;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown1()) {
    /* PROBE_HERE:loop1_body_entry */
    int i = z;
    int j = w;
    int k = 0;
    /*@
      loop invariant i == z + k;
      loop invariant 0 <= k;
      loop invariant i <= j;
      loop assigns i, k;
    */
    /* PROBE_HERE:loop2_before */
    while (i < j) {
      /* PROBE_HERE:loop2_body_entry */
      k++;
      i++;
    }

    x = z;
    y = k;

    if (x % 2 == 1) {
      x++;
      y--;
    }

    /*@
      loop invariant x + y == z + k;
      loop invariant w >= z;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop3_before */
    while (unknown2()) {
      /* PROBE_HERE:loop3_body_entry */
      if (x % 2 == 0) {
        x += 2;
        y -= 2;
      } else {
        x--;
        y--;
      }
    }
    z++;
    w = x + y + 1;
  }

  int c = 0;
  int d = 0;
  /*@
    loop invariant a == b;
    loop invariant c == d;
    loop assigns a, b, c, d;
  */
  /* PROBE_HERE:loop4_before */
  while (unknown3()) {
    /* PROBE_HERE:loop4_body_entry */
    c++;
    d++;
    if (flag) {
      a++;
      b++;
    } else {
      a += c;
      b += d;
    }
  }
  //@ assert(w >= z && a - b == 0);
}
