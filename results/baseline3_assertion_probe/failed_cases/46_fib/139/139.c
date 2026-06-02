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

void main()
{


  int w = 1;
  int z = 0;
  int x = 0;
  int y = 0;

  /*@
    loop invariant w == z + 1;
    loop invariant z == x + y;
    loop invariant x == y;
    loop assigns w, z, x, y;
  */
  /* PROBE_HERE:loop1_before */
  while(unknown1()) {
    /* PROBE_HERE:loop1_body_entry */
	  
    /*@
      loop invariant w == z + 1;
      loop invariant z == x + y;
      loop invariant x == y;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop2_before */
    while(unknown2()){
      /* PROBE_HERE:loop2_body_entry */
      if(w%2 == 1) x++;
      if(z%2 == 0) y++;
    }
    z = x + y;
    w = z + 1;
  }

  
  //@ assert(x == y);
}
