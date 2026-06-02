#include <assert.h>

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();
/*@ assigns \nothing; */
int unknown3();
/*@ assigns \nothing; */
int unknown4();

int main() {

  int w = 1;
  int z = 0;
  int x = 0;
  int y = 0;

  /*@
    loop invariant 0 <= x <= 1;
    loop invariant 1 <= w <= 2;
    loop invariant x == w - 1;
    loop assigns w, z, x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown2()) {
    /* PROBE_HERE:loop1_body_entry */
    if (w % 2 == 1) {
      x++;
      w++;
    }
    if (z % 2 == 0) {
      y++;
      z++;
    }
  }

  //@ assert(x <= 1);
  return 0;
}
