#include <limits.h>
/*@
  ensures INT_MIN <= \result <= INT_MAX;
*/
int unknown_int();

int main() {
    int n;
    int k = 0;
    int i = 0;

    n = unknown_int();

    /*@
      loop invariant 0 <= i;
      loop invariant i <= n;
      loop invariant k == i;
      loop assigns i, k;
    */
    while (i < n) {
        i++;
        k++;
    }

    int j = n;

    /*@
      loop invariant 0 <= j;
      loop invariant j <= n;
      loop invariant k == j;
      loop assigns j, k;
    */
    while (j > 0) {
        //@ assert k > 0;
        j--;
        k--;
    }

    return 0;
}
