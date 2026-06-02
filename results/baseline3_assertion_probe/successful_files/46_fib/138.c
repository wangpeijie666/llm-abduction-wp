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

/*@
  assigns \nothing;
*/
void main(int flag)
{

	int x = 0;
	int y = 0;

	int j = 0;
	int i = 0;

	/*@
	  loop invariant x == y;
	  loop invariant j >= i;
	  loop invariant 0 <= x;
	  loop invariant 0 <= y;
	  loop assigns x, y, i, j;
	*/
	/* PROBE_HERE:loop1_before */
	while(unknown1())
	{
	    /* PROBE_HERE:loop1_body_entry */
	  x++;
	  y++;
	  i += x;
	  j += y;
	  if (flag)
	  	j+=1;
	} 
	//@ assert(j>=i);
	
}
