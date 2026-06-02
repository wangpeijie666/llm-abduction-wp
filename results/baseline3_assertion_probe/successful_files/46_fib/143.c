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

void main() {


  int w = 1;
  int z = 0;
  int x = 0;
  int y = 0;

  /*@
    loop invariant x == y;
    loop invariant w == (1 - (x % 2));
    loop invariant z == (y % 2);
    loop invariant x >= 0 && y >= 0;
    loop assigns w, z, x, y;
  */
  /* PROBE_HERE:loop1_before */
  while(unknown2()){
  	/* PROBE_HERE:loop1_body_entry */
  	if(w) {
  	  x++;
  	  w = !w;
	  }
	
    if(!z) {
      y++; 
      z=!z;
    }
  }

  //@ assert(x==y);
  
}
