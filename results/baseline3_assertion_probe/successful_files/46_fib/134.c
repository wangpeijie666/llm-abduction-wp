#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();
/*@ assigns \nothing; */
int unknown3();
/*@ assigns \nothing; */
int unknown4();

/*
 * IC3 motivating example
 */ 

/*@ assigns \nothing; */
void main()
{
 int x = 1;
 int y = 1;
 /*@
   loop invariant x == y;
   loop invariant x >= 1;
   loop invariant y >= 1;
   loop assigns x, y;
 */
 /* PROBE_HERE:loop1_before */
 while(unknown1()) {
   /* PROBE_HERE:loop1_body_entry */
   int t1 = x;
   int t2 = y;
   x = t1 + t2;
   y = t1 + t2;
 }
 //@ assert(y>=1);
}
