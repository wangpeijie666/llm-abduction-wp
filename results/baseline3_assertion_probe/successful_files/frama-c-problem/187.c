#include <stdio.h>

/*@
  assigns \nothing;
  ensures \result == 1 + (n >= 7 ? 1 + (n - 7) / 3 : 0);
*/
int fun(int n) {
    int i = 7;
    int x = 1;

    /*@
      loop invariant i == 7 + 3*(x-1);
      loop invariant x >= 1;
      loop invariant (i > n) ==> (x == 1 + (n >= 7 ? 1 + (n - 7) / 3 : 0));
      loop assigns i, x;
    */
    /* PROBE_HERE:loop1_before */
    while(i <= n) {
        /* PROBE_HERE:loop1_body_entry */
        x += 1;
        i += 3;
    }
    return x;
}

/*@
  assigns \nothing;
*/
int main() {
    int a = fun(10);
    //@ assert a == 3;
}
