#include <stdio.h>

/*@
  assigns \nothing;
  ensures (a < 0) ==> \result == 0;
  ensures (a >= 0) ==> \result == (a+1) * b;
*/
int mul(int a, int b) {
    int x = a, y = b, prod = 0;

    /*@
      loop invariant a >= 0 ==> x >= -1;
      loop invariant a >= 0 ==> prod == (a - x) * y;
      loop invariant a < 0 ==> (x == a && prod == 0);
      loop assigns x, prod;
    */
    /* PROBE_HERE:loop1_before */
    while(x >= 0) {
        /* PROBE_HERE:loop1_body_entry */
        prod = prod + y;
        x--;
    }
    return prod;
}

/*@ assigns \nothing; */
int main() {
    int pdt = mul(2, 5);
    //@ assert pdt == 15;
}
