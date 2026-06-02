/*@
  requires \true;
  assigns \nothing;
*/
void foo(int y, int z)
{
   int x = 0;

   /*@
     loop invariant 0 <= x <= 5;
     loop invariant (x == 0) || (y <= z);
     loop assigns x, y;
   */
   /* PROBE_HERE:loop1_before */
   while(x < 5) {
      /* PROBE_HERE:loop1_body_entry */
      x += 1;
      if( z <= y) {
         y = z;
      }
   }

   //post-condition
   //@ assert(z >= y);
}
