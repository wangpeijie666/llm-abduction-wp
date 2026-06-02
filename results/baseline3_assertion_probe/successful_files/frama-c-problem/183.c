#include<limits.h>

/*@
  assigns \nothing;
  behavior nonneg:
    assumes x >= 0;
    ensures \result == x;
  behavior neg:
    assumes x < 0;
    ensures \result == 0;
  complete behaviors nonneg, neg;
  disjoint behaviors nonneg, neg;
*/
int test(int x) {
    int a = x;
    int y = 0;

    /*@
      loop invariant y + a == x;
      loop invariant y >= 0;
      loop invariant y + a == x;
      loop assigns a, y;
    */
    /* PROBE_HERE:loop1_before */
    while(a != 0) {
        /* PROBE_HERE:loop1_body_entry */
        y = y + 1;
        a = a - 1;
    }
    return y;
}
    
/*@
  ensures \result == 0;
*/
int main() {
    int num = test(3);
    //@ assert num == 3;
    return 0;
}
