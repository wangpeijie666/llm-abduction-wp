// sum01_true-unreach-call_true-termination.c
#include <limits.h>

/*@
  ensures INT_MIN <= \result <= INT_MAX;
*/
int unknown_int();

int main() {
    int n;
    int i = 0;
    int sn = 0;

    /*@
      loop invariant 1 <= i && i <= n + 1;
      loop invariant sn == (i - 1) * 2;
      loop assigns i, sn;
    */
    for (i = 1; i <= n; i++) {
        sn = sn + (2);
    }

    //@ assert(sn == n * (2) || sn == 0);

    return 0;
}
