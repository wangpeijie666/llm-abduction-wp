/*@ 
  requires n == 10;
  assigns \nothing;
  ensures \result == 30;
*/
int func(int n) {
    int sum = 0;
    int i = 0;

    /*@
      loop invariant 0 <= i;
      loop invariant i <= n/2 + 1;
      loop invariant sum == i*(i-1);
      loop assigns i, sum;
    */
    /* PROBE_HERE:loop1_before */
    while(i <= n/2) {
        /* PROBE_HERE:loop1_body_entry */
        sum = sum + 2*(i);
        i++;
    }
    return sum;
}

// write a test
void main() {
    int t = func(10);
    //@ assert t == 30;
}
