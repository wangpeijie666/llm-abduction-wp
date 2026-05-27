//terminator_03_true-unreach-call_true-termination.c

/*@
    ensures \result == 0;
*/
int main() {
	int x;
	int y;

	/*@
        loop invariant x <= 100;
        loop invariant y > 0;
        loop invariant x >= 0; // Assuming x starts from a non-negative value
        loop assigns x;
    */
	if (y > 0) {
		/* PROBE_HERE:loop1_before */
		while (x < 100) {
			/* PROBE_HERE:loop1_body_entry */
			x = x + y;
		}
	}
	
	//@ assert(y <= 0 || (y > 0 && x >= 100));

	return 0;
}
