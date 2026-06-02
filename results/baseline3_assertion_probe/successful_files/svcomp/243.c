int main() {
    int i;
    int j;

    int x = i;
    int y = j;
    /*@
      loop invariant x - y == i - j;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop1_before */
    while (x != 0) {
    	/* PROBE_HERE:loop1_body_entry */
    	x--;
    	y--;
    }

    if (i == j) {
    	//@ assert(y == 0);
    }
    
    return 0;
}
