#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*@
  assigns \nothing;
*/
void foo(int n)
{
  int x=0;
  int y=0;
  int i=0;
  
  /*@
    loop invariant 0 <= i;
    loop invariant x == i;
    loop invariant 0 <= y <= i;
    loop invariant y == (i/2);
    loop assigns i, x, y;
  */
  /* PROBE_HERE:loop1_before */
  while(i<n) {
    /* PROBE_HERE:loop1_body_entry */
    i++;
    x++;
    if(i%2 == 0) y++;
  }
  
  if(i%2 == 0) {
    //@ assert(x==2*y);
  }
}
