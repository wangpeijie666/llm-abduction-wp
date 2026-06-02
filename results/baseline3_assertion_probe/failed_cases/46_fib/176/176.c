#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*
 * Based on ex16 from NECLA Static Analysis Benchmarks
 */

/*@
  assigns \nothing;
*/
int unknown1();

/*@
  assigns \nothing;
*/
int unknown2();

/*@
  assigns \nothing;
*/
int unknown3();

/*@
  assigns \nothing;
*/
int unknown4();

/*@
  assigns y;
*/
int foo(int x, int y)
{
  int i=0;
  int t=y;
   
  if (x==y) return x;
  
  /*@
    loop invariant y >= t;
    loop assigns y;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown1()){
    /* PROBE_HERE:loop1_body_entry */
    if (x > 0)   
      y = y + x;
  }
   
  //@ assert(y >= t);
  return 0;
}
