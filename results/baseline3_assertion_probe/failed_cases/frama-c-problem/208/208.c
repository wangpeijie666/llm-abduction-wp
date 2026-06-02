#include <stdio.h>
#include <math.h>

/*@
  assigns \nothing;
  ensures \result == 7;
*/
int fun(int n) {
    double y = 0;
    double i = 0;

    /*@
      loop invariant i == 0.0;
      loop invariant y == 0.0;
      loop assigns y, i;
    */
    /* PROBE_HERE:loop1_before */
    while(i <= n) {
        /* PROBE_HERE:loop1_body_entry */
        y = y + pow(2.0, i);
        i = i + 1;
    }
    return y;
}

int main() {
    int res = fun(4);
    //@ assert res == 7;
}
