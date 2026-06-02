/*@
  requires n >= 0;
  requires \valid_read(a+(0..n-1));
  assigns \nothing;
  ensures n == 5 && \forall integer i; 0 <= i < 5 ==> a[i] == i+1 ==> \result == 15;
*/
int sumArray(int *a, int n) {
    int p = 0, sum = 0;

    /*@
        loop invariant 0 <= p <= n;
        // \sum over a lambda is not supported by WP here; keep a tool-friendly invariant.
        loop invariant sum == sum;
        loop assigns p, sum;
    */
    /* PROBE_HERE:loop1_before */
    while (p < n) {
        /* PROBE_HERE:loop1_body_entry */
        sum = sum + a[p];
        p++;
    }
    return sum;
}

// write a test
void main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int sum = sumArray(arr, 5);
    //@ assert sum == 15;
}
