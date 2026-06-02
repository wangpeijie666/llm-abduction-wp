#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*@
requires flag > 0;
assigns \nothing;
*/
void foo(int flag, int a) {
   int b;
   int j = 0;
   /*@
     loop invariant 0 <= b <= 100;
     loop invariant j == b;
     loop assigns b, j;
   */
   /* PROBE_HERE:loop1_before */
   for (b = 0; b < 100 ; ++b){
      /* PROBE_HERE:loop1_body_entry */
      if (flag)
         j = j + 1;
   }

   if(flag) {
      //@ assert(j==100);
   }
}
