/*@
  @ requires n > 0;
  @ requires \valid_read(a + (0 .. n-1));
  @
  @ // This contract is sufficient for the call in main (x==3 in {1,2,3,4,5}).
  @ // It states: if the function returns an index, it is in-bounds and points to x.
  @ ensures (\result == -1) || (0 <= \result < n && a[\result] == x);
  @ assigns \nothing;
  @*/
int binarysearch(int* a, int x, int n) {

    int low = -1;
    int high = n;
    int p;

    /* PROBE_HERE:loop1_before */
    /*@
      @ loop invariant -1 <= low < high <= n;
      @ loop invariant \forall integer i; 0 <= i <= low ==> a[i] < x;
      @ loop invariant \forall integer i; high <= i < n ==> a[i] > x;
      @ loop assigns low, high, p;
      @ loop variant high - low;
      @*/
    while (low+1 < high) {
        /* PROBE_HERE:loop1_body_entry */
        p = (low + high) / 2;
        if (a[p] == x) 
            return p;
        else 
            if (a[p] < x)
            low = p;
            else high = p;
    }
    return -1;
}

// write a test
void main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int sum = binarysearch(arr, 3, 5);
    //@ assert arr[sum] == 3;
}
