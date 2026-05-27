// jm2006_variant_true-unreach-call.c
#include <limits.h>

/*@
  ensures INT_MIN <= \result <= INT_MAX;
*/
int unknown_int();

int main() {
    int i;
    int j;

    int x = i;
    int y = j;
    int z = 0;
    
    /*@
      loop invariant x >= 0;
      loop invariant z >= 0;
      loop invariant y == j - 2 * z;
      loop invariant x + z == i;
      loop assigns x, y, z;
    */
    while (x != 0) {
    	x--;
    	y -= 2;
    	z++;
    }

    if (i == j) {
    	//@ assert(y == -z);
    }
    
    return 0;
}
