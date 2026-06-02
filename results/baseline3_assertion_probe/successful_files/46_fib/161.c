#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();


/*
 * From CAV'12 by Sharma et al.
 */

/*@ assigns \nothing; */
int unknown();

void main() {
  int x = 0;
  int y = 0;
  int n = 0;
  /*@
    loop invariant x == y;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while(unknown()) {
      /* PROBE_HERE:loop1_body_entry */
      x++;
      y++;
  }
  /*@
    loop invariant x - n == y - n;
    loop invariant x == y;
    loop assigns x, y;
  */
  /* PROBE_HERE:loop2_before */
  while(x!=n) {
      /* PROBE_HERE:loop2_body_entry */
      x--;
      y--;
  }
  //@ assert(y==n);
}
