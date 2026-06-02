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
 * "nested5.c" from InvGen test suite
 */

/*@
  assigns \nothing;
*/
void main() {
  int i,j,k,n;
  
  /*@
    loop invariant 0 <= i;
    loop invariant \forall integer ii; 0 <= ii < i ==>
                    (\forall integer jj; ii <= jj < n ==>
                      (\forall integer kk; jj <= kk < n ==> kk >= ii));
    loop assigns i, j, k;
  */
  /* PROBE_HERE:loop1_before */
  for (i=0;i<n;i++)
    /*@
      loop invariant i <= j;
      loop invariant \forall integer jj; i <= jj < j ==>
                      (\forall integer kk; jj <= kk < n ==> kk >= i);
      loop assigns j, k;
    */
    /* PROBE_HERE:loop2_before */
    for (j=i;j<n;j++)
      /*@
        loop invariant j <= k;
        loop invariant k >= j;
        loop invariant j >= i;
        loop invariant k >= i;
        loop assigns k;
      */
      /* PROBE_HERE:loop3_before */
      for (k=j;k<n;k++){
	      /* PROBE_HERE:loop3_body_entry */
	      //@ assert(k>=i);
      }
}
