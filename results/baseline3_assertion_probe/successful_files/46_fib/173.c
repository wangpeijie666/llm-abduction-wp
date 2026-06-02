#include <assert.h>
int unknown1();
int unknown2();

/*@
  requires flag > 0;
  assigns \nothing;
*/
void foo(int flag) {
  int i, j, k;
  j = 1;
  if (flag) {
    i = 0;
  } else {
    i = 1;
  }

  /*@
    loop invariant i % 2 == 0;
    loop invariant j == i + 1;
    loop assigns i, j;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown1()) {
    /* PROBE_HERE:loop1_body_entry */
    i += 2;
    if (i % 2 == 0) {
      j += 2;
    } else j++;
  }

  int a = 0;
  int b = 0;

  /*@
    loop invariant a >= 0;
    loop invariant b == a * (j - i);
    loop assigns a, b;
  */
  /* PROBE_HERE:loop2_before */
  while (unknown2()) {
    /* PROBE_HERE:loop2_body_entry */
    a++;
    b += (j - i);
  }
  if (flag) {
    //@ assert(a == b);
  }
}
