/*@
  assigns \nothing;
  ensures \result >= 0;
  ensures \old(num) == 123 ==> \result == 6;
  ensures \old(num) != 123 ==> \result >= 0;
*/
int func(int num) {
    int i = 0;
    int sum = 0;

    /*@
      loop invariant sum >= 0;
      loop invariant sum >= 0;
      loop assigns num, i, sum;
    */
    /* PROBE_HERE:loop1_before */
    while(num>0) {
        /* PROBE_HERE:loop1_body_entry */
        i = num%10;
        sum += i;
        num /= 10;
    }
    return sum;
}

// write a test
/*@
  assigns \nothing;
*/
void main() {
    int t = func(123);
    //@ assert t == 6;
}
