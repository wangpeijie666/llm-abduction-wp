//terminator_03_true-unreach-call_true-termination.c
#include <limits.h>

/*@
  ensures INT_MIN <= \result <= INT_MAX;
*/
int unknown_int();

int main() {
	int x;
	int y;
	if (y > 0) {
		/*@
		  loop invariant x < 100;
		  loop invariant y > 0;
		  loop assigns x;
		*/
		while (x < 100) {
			x = x + y;
		}
	}
	
	//@ assert(y <= 0 || (y > 0 && x >= 100));

	return 0;
}
