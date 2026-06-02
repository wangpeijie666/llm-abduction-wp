#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*@
  requires \true;
  assigns \nothing;
*/
int unknown1();
/*@
  requires \true;
  assigns \nothing;
*/
int unknown2();
/*@
  requires \true;
  assigns \nothing;
*/
int unknown3();
/*@
  requires \true;
  assigns \nothing;
*/
int unknown4();


/*@
  requires \true;
  assigns \nothing;
*/
void foo(int flag) {
   int j = 2; 
   int k = 0;

   /*@
     loop invariant j >= 2;
     loop invariant k >= 0;
     loop invariant (flag == 0) ==> (j == 2 * k + 2);
     loop invariant (k != 0) ==> (flag == 0);
     loop assigns j, k;
   */
   /* PROBE_HERE:loop1_before */
   while(unknown1()){ 
     /* PROBE_HERE:loop1_body_entry */
     if (flag)
       j = j + 4;
     else {
       j = j + 2;
       k = k + 1;
     }
   }
   if(k != 0) {
     //@ assert(j == 2 * k + 2);
   }
}
