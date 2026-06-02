#include <assert.h>

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();
/*@ assigns \nothing; */
int unknown3();
/*@ assigns \nothing; */
int unknown4();

/*@
  assigns \nothing;
*/
void foo(int flag) {
  int x = 0;
  int y = 0;
  int j = 0;
  int i = 0;

  /*@
    loop invariant 0 <= x;
    loop invariant 0 <= y;
    loop invariant x == y;
    loop invariant i <= j;
    loop invariant i <= j + 1;
    loop invariant x == 0 ==> y == 0;
    loop assigns x, y, i, j;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown1()) {
    /* PROBE_HERE:loop1_body_entry */
    x++;
    y++;
    i += x;
    j += y;
    if (flag) {
      j += 1;
    }
  }
  if (j >= i)
    x = y;
  else
    x = y + 1;

  int w = 1;
  int z = 0;
  /*@
    loop invariant w == z + 1;
    loop invariant x == y;
    loop assigns w, z, x, y;
  */
  /* PROBE_HERE:loop2_before */
  while (unknown2()) {
    /* PROBE_HERE:loop2_body_entry */
    /*@
      loop invariant w == z + 1;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop3_before */
    while (unknown3()) {
      /* PROBE_HERE:loop3_body_entry */
      if (w % 2 == 1)
        x++;
      if (z % 2 == 0)
        y++;
    }
    z = x + y;
    w = z + 1;
  }
  //@ assert(x == y);
}
