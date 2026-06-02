int unknown1();
int unknown2();
int unknown3();

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
void foo(int k)
{
  int z = k;
  int x = 0;
  int y = 0;

  /*@
    loop invariant x == y;
    loop invariant z == k + y;
    loop assigns z, x, y;
  */
  /* PROBE_HERE:loop1_before */
  while(unknown1())
  {
      /* PROBE_HERE:loop1_body_entry */
    int c = 0;
    /*@
      loop invariant x == y;
      loop invariant z == k + y - c;
      loop invariant c >= 0;
      loop assigns x, y, c;
    */
    /* PROBE_HERE:loop2_before */
    while(unknown2())
    {
        /* PROBE_HERE:loop2_body_entry */
      if(z==k+y-c)
      {
        x++;
        y++;
        c++;
      }else
      {
        x++;
        y--;
        c++;
      }
    }
    /*@
      loop invariant x == y;
      loop invariant c >= 0;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop3_before */
    while(unknown3())
    {
        /* PROBE_HERE:loop3_body_entry */
      x--;
      y--;
    }
    z=k+y;
  }
  //@ assert(x==y);
}
