#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

/*@ 
  requires n > 0;
  assigns \nothing;
*/
void foo(int n) {

  int i, a, b;
  i = 0; a = 0; b = 0;
  /*@
    loop invariant 0 <= i <= n;
    loop invariant a >= 0 && b >= 0;
    loop invariant a + b == 3*i;
    loop assigns i, a, b;
  */
  /* PROBE_HERE:loop1_before */
  while( i < n ) {
    /* PROBE_HERE:loop1_body_entry */
    if(unknown1()) {
      a = a + 1;
      b = b + 2;
    } else {
      a = a + 2;
      b = b + 1;
    }
    i = i + 1;
  }
  //@ assert( a + b == 3*n );
}
