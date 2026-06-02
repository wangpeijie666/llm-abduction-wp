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
 int k=1;
 int i=1;
 int j=0;
 /*@
   loop invariant 1 <= i;
   loop invariant k >= 1;
   loop invariant k >= i;
   loop assigns i, j, k;
 */
 /* PROBE_HERE:loop1_before */
 while(i < n) {
  /* PROBE_HERE:loop1_body_entry */
  j = 0;
  /*@
    loop invariant 0 <= j <= i;
    loop invariant k >= 1;
    loop assigns j, k;
  */
  /* PROBE_HERE:loop2_before */
  while(j < i) {
      /* PROBE_HERE:loop2_body_entry */
      k += (i-j);
      j++;
  }
  i++;
 }
 //@ assert(k >= n);
 
}
