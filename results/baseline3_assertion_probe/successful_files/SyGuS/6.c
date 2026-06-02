int main()
{
   int x = 0;
   int size;
   int y, z;

   /*@
      loop invariant 0 <= x;
      loop invariant \true;
      loop invariant x == 0 ==> \true; // was: y == z (not established initially)
      loop invariant x > 0 ==> y <= z;
      loop assigns x, y;
   */
   /* PROBE_HERE:loop1_before */
   while(x < size) {
      /* PROBE_HERE:loop1_body_entry */
      x += 1;
      if( z <= y) {
         y = z;
      }
   }

   //post-condition
   if(size > 0) {
      //@ assert(z >= y);
   }
}
