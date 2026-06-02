#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*@
  assigns \nothing;
*/
void main()
{
  int x = 0;
  int y = 0;
  int z = 0;
  int k = 0;

  /*@
    // Generated relational invariants were not inductive: x is not incremented on every iteration
    // (only when k%3==0) while y and z are always incremented.
    // Keep only simple, inductive invariants.
    loop invariant y == z;
    loop invariant x <= y;
    loop invariant x == y;
    loop assigns x, y, z, k;
  */
  /* PROBE_HERE:loop1_before */
  while(unknown1())
  {
      /* PROBE_HERE:loop1_body_entry */
     if(k%3 == 0)
       x++;
     y++;
     z++;
     k = x+y+z;
  }

  //@ assert(x==y);
  //@ assert(y==z);
 
}
