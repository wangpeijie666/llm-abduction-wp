//terminator_03_true-unreach-call_true-termination.c
int main() {
	int x;
	int y;
	/*@
		assigns x, y;
	*/
	if (y > 0) {
		/*@
			loop invariant y > 0;
			loop invariant \true;
			loop assigns x;
		*/
		/* PROBE_HERE:loop1_before */
		while (x < 100) {
			/* PROBE_HERE:loop1_body_entry */
			x = x + y;
		}
	}
	

	//@ assert(y <= 0 || (y > 0 && x >= 100));

	return 0;
}
