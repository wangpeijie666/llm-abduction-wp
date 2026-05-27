int main() {
    int i;
    int j;

    int x = i;
    int y = j;

    /*@
        loop invariant x >= 0;
        loop invariant y == j - (i - x);
        loop assigns x, y;
    */
    /* PROBE_HERE:loop1_before */
    while (x != 0) {
    	/* PROBE_HERE:loop1_body_entry */
    	x--;
    	y--;
    }

    /*@
        requires i == j;
        ensures y == 0;
    */
    if (i == j) {
    	//@ assert(y == 0);
    }
    
    return 0;
}
