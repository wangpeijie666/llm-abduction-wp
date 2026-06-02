#include<assert.h>

int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*@
requires (x + y) == k;
requires n > 0;
assigns \nothing;
ensures (x + y) == k;
*/
void foo(int x, int y, int k, int j, int i, int n) {
  int m = 0;
  j = 0;
  /*@
    loop invariant 0 <= j <= n;
    loop invariant (x + y) == k;
    loop invariant 0 <= m <= j;
    loop invariant m < n;
    loop invariant j < n ==> m < n;
    loop assigns x, y, j, m;
  */
  /* PROBE_HERE:loop1_before */
  while (j < n) {
    /* PROBE_HERE:loop1_body_entry */
    if (j == i) {
      x++;
      y--;
    } else {
      y++;
      x--;
    }
    if (unknown1())
      m = j;
    j++;
  }
  //@ assert((x + y) == k);
  
  if (n > 0) {
    //@ assert(0 <= m);
    //@ assert(m < n);
  }

}
