int arraysearch(int* a, int x, int n) { 

  /*@
    requires n >= 0;
    requires \valid_read(a+(0..n-1));
    assigns \nothing;
    ensures \result == 0 || \result == 1;
    ensures \result == 1 <==> (\exists integer i; 0 <= i < n && a[i] == x);
    ensures \result == 0 <==> (\forall integer i; 0 <= i < n ==> a[i] != x);
  */
  /* PROBE_HERE:loop1_before */
  for (int p = 0; p < n; p++) {
    /* PROBE_HERE:loop1_body_entry */
    // STart
    /*@
      loop invariant 0 <= p <= n;
      loop invariant \forall integer i; 0 <= i < p ==> a[i] != x;
      loop assigns p;
    */
    if (x == a[p]) 
       return 1;
    // End
  }
  return 0;
}

// write a test
void main() {
  int arr[5] = {1, 2, 3, 4, 5};
  int sum = arraysearch(arr, 3, 5);
  //@ assert sum == 1;
}
