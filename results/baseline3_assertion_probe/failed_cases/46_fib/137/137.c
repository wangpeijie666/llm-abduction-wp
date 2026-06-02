#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();


void main() {
  int x, y;

  x = -50;
  /*@
    // The previous invariant `x <= 99` is not inductive (x := x + y with unconstrained y).
    // Keep only facts that are preserved and useful at loop exit.
    loop invariant \true;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while( x < 0 ) {
      /* PROBE_HERE:loop1_body_entry */
	x = x + y;
	y++;
  }
  //@ assert(y > 0);
}
