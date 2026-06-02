#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*
 * Based on "SYNERGY: A New Algorithm for Property Checking" by Gulavani et al.
 */

/*@
  ensures \result == 0;
*/
int main() {

  int i, c;
  i = 0;
  c = 0;
  /*@
    loop invariant 0 <= i <= 1000;
    loop invariant c >= 0;
    loop invariant c == (i * (i - 1)) / 2;
    loop assigns i, c;
  */
  /* PROBE_HERE:loop1_before */
  while (i < 1000) {
    /* PROBE_HERE:loop1_body_entry */
    c = c + i;
    i = i + 1;
  }

  //@ assert(c >= 0);
}
