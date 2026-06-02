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

void main()
{
  int x = 0;
  int y = 0;
  int i = 0;
  int j = 0;

  /*@
    loop invariant x == y;
    loop invariant i >= j;
    loop assigns x, y, i, j;
  */
  /* PROBE_HERE:loop1_before */
  while(unknown1())
  {
      /* PROBE_HERE:loop1_body_entry */
    /*@
      loop invariant x == y;
      loop invariant i >= j;
      loop assigns i, j;
    */
    /* PROBE_HERE:loop2_before */
    while(unknown2())
    {
        /* PROBE_HERE:loop2_body_entry */
       if(x == y)
          i++;
       else
          j++;
    }
    if(i >= j)
    {
       x++;
       y++;
    }
    else
       y++;
  }

  //@ assert(i >= j);
}
