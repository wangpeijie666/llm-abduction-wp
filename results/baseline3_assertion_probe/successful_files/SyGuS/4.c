/*@
  assigns \nothing;
*/
void foo(int y, int z)
{
   int x = 0;

   /*@
     loop invariant 0 <= x <= 500;
     loop invariant (y <= z) || (x == 0);
     loop assigns x, y;
   */
   /* PROBE_HERE:loop1_before */
   while(x < 500) {
      /* PROBE_HERE:loop1_body_entry */
      x += 1;
      if( z <= y) {
         y = z;
      }
   }

   //post-condition
   //@ assert(z >= y);
}
