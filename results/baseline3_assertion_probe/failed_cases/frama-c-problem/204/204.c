int arraySearch(int *a, int x, int n) {
    /*@ requires 0 <= n;
        requires \valid_read(a + (0 .. n-1));
        assigns \nothing;
    */
    int p = 0;

    /*@ 
        loop invariant 0 <= p;
        loop invariant \forall integer i; 0 <= i < p ==> a[i] != x;
        loop assigns p;
    */
    /* PROBE_HERE:loop1_before */
    while (p < n) {
        /* PROBE_HERE:loop1_body_entry */
        if (a[p] == x) {
            return 1;
        }
        p++;
    }
    return 0;
}

// write a test
void main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int sum = arraySearch(arr, 3, 5);
    //@ assert sum == 1;
}
