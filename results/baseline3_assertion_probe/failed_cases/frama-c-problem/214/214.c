// This program used an advanced ACSL clause: \max()
// Note: Some versions of 'wp' plugin may not support the \lambda clause.
//       The program may not verify in every machine.

/*@
  requires n > 0;
  requires \valid_read(arr+(0..n-1));
  assigns \nothing;
  ensures \forall integer i; 0 <= i < n ==> \result >= arr[i];
  ensures \exists integer i; 0 <= i < n && \result == arr[i];
*/
int array_max_advanced(int* arr, int n) {
    int max = arr[0];
    /*@
      loop invariant 0 <= i <= n;
      loop invariant \forall integer k; 0 <= k < i ==> max >= arr[k];
      loop invariant \exists integer k; 0 <= k < i+1 && max == arr[k];
      loop invariant max >= arr[0];
      loop invariant i == n ==> (\forall integer k; 0 <= k < n ==> max >= arr[k]);
      loop assigns i, max;
    */
    /* PROBE_HERE:loop1_before */
    for (int i = 0; i < n; i++) {
        /* PROBE_HERE:loop1_body_entry */
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

// write a test
void main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int max = array_max_advanced(arr, 5);
    //@ assert max >= arr[0];
    //@ assert max >= arr[1];
    //@ assert max >= arr[2];
    //@ assert max >= arr[3];
    //@ assert max >= arr[4];
}
