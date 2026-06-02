#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*
 * From "Simplifying Loop Invariant Generation using Splitter Predicates", Sharma et al. CAV'11
 */

/*@
requires n >= 0;
requires m >= 0;
requires m < n;
assigns \nothing;
ensures \true;
*/
void foo(int n, int m)
{
  int x = 0; 
  int y = m;
  /*@
    loop invariant 0 <= x <= n;
    loop invariant y == m + (x > m ? (x - m) : 0);
    loop assigns x, y;
  */
  /* PROBE_HERE:loop1_before */
  while(x < n) {
    /* PROBE_HERE:loop1_body_entry */
    x++;
    if(x > m) y++;
  }
  //@ assert(y==n);
}
