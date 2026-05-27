//terminator_03_true-unreach-call_true-termination.c

/*@
  requires \true;
  assigns \nothing;
*/
int main() {
	int x;
	int y;

	/*@
	  loop invariant y > 0 ==> x <= 100;
	  loop invariant y > 0 ==> x >= 0;
	  loop invariant y > 0 ==> \exists integer k; k >= 0 && x == \at(x, Pre) + k * y;
	  loop assigns x;
	  loop variant 100 - x;
	*/
	if (y > 0) {
		while (x < 100) {
			x = x + y;
		}
	}

	//@ assert(y <= 0 || (y > 0 && x >= 100));

	return 0;
}
