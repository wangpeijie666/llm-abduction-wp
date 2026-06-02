#include <assert.h>
int unknown1();
int unknown2();
int unknown3();

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();
/*@ assigns \nothing; */
int unknown3();

/*
 *  Based on "Automatically refining abstract interpretations" fig.1
 */


void main() {
 int x = 0, y = 0;
 /*@
   loop invariant x >= 0;
   loop invariant y >= 0;
   loop invariant (x < 4) || (y > 2);
   loop assigns x, y;
 */
 /* PROBE_HERE:loop1_before */
 while(unknown1()) {
   /* PROBE_HERE:loop1_body_entry */
   if(unknown2()) { 
      x++; 
      y += 100; 
   }
   else if (unknown3()){ 
      if (x >= 4) { 
          x++; 
          y++; 
      } 
      if (x < 0) {
          y--;
      }
   }
  
 }
 //@ assert(x < 4 || y > 2);
}
