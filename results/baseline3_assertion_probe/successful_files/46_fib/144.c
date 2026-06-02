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
  int j = 0;
  int i;
  int x = 100;
   
  /*@
    loop invariant 0 <= i <= x;
    loop invariant j == 2*i;
    loop assigns i, j;
  */
  /* PROBE_HERE:loop1_before */
  for (i = 0; i < x ; i++){
    /* PROBE_HERE:loop1_body_entry */
    j = j + 2;
  }

  //@ assert(j == 2*x);
}
