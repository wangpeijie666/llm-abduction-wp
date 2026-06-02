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
int main()
{
	int i = 1;
	int j = 0;
	int z = i - j;
	int x = 0;
	int y = 0;
	int w = 0;

	/*@
	  loop assigns z, y, x, w;
	  loop invariant y >= 0;
	  loop invariant x <= y;
	  loop invariant y >= 0;
	  loop invariant w == 2*y;
	  // This loop invariant is the missing fact needed to prove x==y at loop exit.
	  // It is NOT supported by the loop body unless additional program assumptions hold.
	  loop invariant x == y;
	*/
	/* PROBE_HERE:loop1_before */
	while(unknown2()) 
	{
	    /* PROBE_HERE:loop1_body_entry */
		z += x + y + w;
		y++;
		if (z % 2 == 1) 
		  x++;
		w += 2; 
	}

	/*@ assert x <= y; */
	//@ assert(x==y);
}
