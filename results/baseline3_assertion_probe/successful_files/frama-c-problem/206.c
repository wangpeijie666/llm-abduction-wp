#include <stdlib.h>

/*@
    requires n >= 0;
    assigns \nothing;
    ensures \result == (n * (n + 1)) / 2;
*/
int sum(int n) {
    int s = 0;
    int k = 0;

    /*@
      loop invariant 0 <= k <= n + 1;
      loop invariant s == (k * (k - 1)) / 2;
      loop assigns s, k;
    */
    /* PROBE_HERE:loop1_before */
    while(k <= n) {    
        /* PROBE_HERE:loop1_body_entry */
        s = s + k;
        k = k + 1;
    }
    return s;
}

/*@
  assigns \nothing;
  ensures \result == 0;
*/
int main() {
    int s = sum(5);
    //@ assert s == 15;
}
