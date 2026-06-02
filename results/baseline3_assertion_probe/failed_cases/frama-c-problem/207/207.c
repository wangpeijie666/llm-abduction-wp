#include <stdio.h>

/*@
  ensures \result == (c > 0 ? c : 0);
  ensures \result >= 0;
  assigns \nothing;
*/
int func(int c) {
    int x = c;
    int y = 0;

    /*@
      loop invariant x + y == c;
      loop invariant y >= 0;
      loop invariant x <= c;
      loop invariant y >= c ==> x <= 0;
      loop assigns x, y;
    */
    /* PROBE_HERE:loop1_before */
    while(x > 0) {
        /* PROBE_HERE:loop1_body_entry */
        x = x - 1;
        y = y + 1;
    }
    return y;
}

// write a test
void main() {
    int t = func(5);
    //@ assert t == 5;
}
