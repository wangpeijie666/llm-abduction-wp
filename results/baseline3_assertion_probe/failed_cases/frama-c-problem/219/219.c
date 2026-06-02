void func(int *a, int n) {
    /*@
        requires n >= 0;
        requires \valid(a + (0..n-1));
        assigns a[0..n-1];
        ensures \forall integer k; 0 <= k < n && k % 2 == 0 ==> a[k] == 0;
    */
    /* PROBE_HERE:loop1_before */
    for (int i = 0; i < n; i++) {
        /* PROBE_HERE:loop1_body_entry */
        /*@
            loop invariant 0 <= i <= n;
            loop invariant \forall integer k; 0 <= k < i && k % 2 == 0 ==> a[k] == 0;
            loop assigns i, a[0..n-1];
        */
        if (i%2==0) 
            a[i] = 0;
    }
}

// write a test
void main() {
    int arr[5] = {1, 2, 3, 4, 5};
    func(arr, 5);
    //@ assert arr[0] == 0;
    //@ assert arr[2] == 0;
    //@ assert arr[4] == 0;
}
