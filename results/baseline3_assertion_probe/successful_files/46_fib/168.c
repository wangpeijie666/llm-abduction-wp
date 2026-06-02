#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

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

/*
 * InvGen, CAV'09 paper, fig 2
 */
/*@
requires n > 0;
assigns \nothing;
ensures \true;
*/
void foo(int n) {
  int x= 0;
  /*@
    loop invariant 0 <= x <= n;
    loop assigns x;
  */
  /* PROBE_HERE:loop1_before */
  while(x<n) {
    /* PROBE_HERE:loop1_body_entry */
    x++;
  } 
  if(n>0) {
    //@ assert(x==n);
  }
}
