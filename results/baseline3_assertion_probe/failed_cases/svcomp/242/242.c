// jm2006_variant_true-unreach-call.c

/*@
    ensures 
    \result == 0;
*/
int main() {
    int i;
    int j;

    int x = i;
    int y = j;
    int z = 0;

    /*@
        loop invariant x >= 0 || x == i;
        loop invariant z <= i;
        loop invariant z >= 0;
        loop invariant y == j - 2 * z;
        loop invariant x + z == i;
        loop assigns x, y, z;
    */
    /* PROBE_HERE:loop1_before */
    while (x != 0) {
        /* PROBE_HERE:loop1_body_entry */
        x--;
        y -= 2;
        z++;
    }

    if (i == j) {
        //@ assert y == -z;
    }

    return 0;
}
