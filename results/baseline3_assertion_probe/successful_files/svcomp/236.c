/*@
	requires n >= 0;
	ensures \true;
*/
void foo(int n){
	int x = n;
	int y = 0;

	/*@
		loop invariant 0 <= x <= n;
		loop invariant y == n - x;
		loop assigns x, y;
	*/
	/* PROBE_HERE:loop1_before */
	while (x > 0) {
		/* PROBE_HERE:loop1_body_entry */
		x--;
		y++;
	}

	//@ assert(y == n);
}
