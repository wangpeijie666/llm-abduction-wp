#include <assert.h>

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();
/*@ assigns \nothing; */
int unknown3();
/*@ assigns \nothing; */
int unknown4();

void main() {
  int w = 1, z = 0, x = 0, y = 0;
  /*@
    loop invariant x == y;
    // NOTE: w and z are only (re)related after the unknown4() loop executes.
    // During the unknown2() loop, x/y may change while w/z stay unchanged,
    // so relations like w==z+1 or z==x+y are not inductive for this outer loop.

    loop assigns w, z, x, y;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown1()) {
    /* PROBE_HERE:loop1_body_entry */
    /*@
      loop invariant x == y;
      // w and z are not modified in this loop, so relating them here is not inductive
      loop assigns x, y;
    */
    /* PROBE_HERE:loop2_before */
    while (unknown2()) {
      /* PROBE_HERE:loop2_body_entry */
      if (w % 2 == 1)
        x++;
      if (z % 2 == 0)
        y++;
    }
    /*@
      loop invariant x == y;
      loop assigns w, z;
    */
    /* PROBE_HERE:loop3_before */
    while (unknown4()) {
      /* PROBE_HERE:loop3_body_entry */
      z = x + y;
      w = z + 1;
    }
  }
  //@ assert(x == y);
}
