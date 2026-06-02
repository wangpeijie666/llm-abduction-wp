// Program to find index of an element in an array
// Behaviors not used in this program

/*@
  requires n >= 0;
  requires \valid_read(arr+(0..n-1));
  assigns \nothing;
  ensures -1 <= \result < n;
  ensures \result == -1 ==> \forall integer k; 0 <= k < n ==> arr[k] != x;
  ensures \result != -1 ==> arr[\result] == x;
  ensures \result != -1 ==> \forall integer k; 0 <= k < \result ==> arr[k] != x;
*/
int array_find(int* arr, int n, int x) {
    int i = 0;

    /*@
      loop invariant 0 <= i <= n;
      loop invariant \forall integer k; 0 <= k < i ==> arr[k] != x;
      loop assigns i;
    */
    /* PROBE_HERE:loop1_before */
    for (i = 0; i < n; i++) {
        /* PROBE_HERE:loop1_body_entry */
        if (arr[i] == x) {
            return i;
        }
    }
    return -1;
}

// write a test
void main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int index = array_find(arr, 5, 3);
    //@ assert index == 2;
}
