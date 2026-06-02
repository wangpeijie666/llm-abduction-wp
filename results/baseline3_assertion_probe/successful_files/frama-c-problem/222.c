#include <stdio.h>

/*@
    requires n <= 0 || \valid(a + (0..n-1));
    assigns a[0..n-1];
    ensures \forall integer k; 0 <= k < n-1 ==> a[k] <= a[k+1];
*/
void bubbleSort(int *a, int n) {
    if (n <= 0) return;
    int i, j, temp;

    /*@
      loop invariant 0 <= i <= n-1;
      loop invariant \forall integer k; i+1 <= k <= n-1 ==> (\forall integer t; 0 <= t < k ==> a[t] <= a[k]);
      loop assigns i, j, temp, a[0..n-1];
    */
    /* PROBE_HERE:loop1_before */
    for(i=n-1; i>0; i--) {
        /* PROBE_HERE:loop1_body_entry */
        /*@
          loop invariant 0 <= j <= i;
          loop invariant \forall integer k; i+1 <= k <= n-1 ==> (\forall integer t; 0 <= t < k ==> a[t] <= a[k]);
          loop invariant \forall integer t; 0 <= t < j ==> a[t] <= a[j];
          loop assigns j, temp, a[0..i];
        */
        /* PROBE_HERE:loop2_before */
        for(j=0; j<i; j++) {
            /* PROBE_HERE:loop2_body_entry */
            if (a[j] > a[j+1]) {
                temp = a[j];
                a[j] = a[j+1];
                a[j+1] = temp;
            }
        }
    }
}

// write a test
/*@
  assigns \nothing;
*/
void main() {
    int arr[5] = {5, 4, 3, 2, 1};
    bubbleSort(arr, 5);
    //@ assert \forall int i; 0 <= i < 4 ==> arr[i] <= arr[i+1];
}
