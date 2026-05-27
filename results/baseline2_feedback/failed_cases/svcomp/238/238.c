#include <limits.h>

/*@
    ensures \result >= INT_MIN && \result <= INT_MAX;
*/
int unknown_int();

int main() {
    unsigned int i, j, a, b;
    int flag = unknown_int();
    a = 0;
    b = 0;
    j = 1;
    if (flag) {
        i = 0;
    } else {
        i = 1;
    }

    /*@
      loop invariant a >= 0;
      loop invariant b >= 0;
      loop invariant i >= 0;
      loop invariant j >= 1;
      loop assigns a, b, i, j;
    */
    while (unknown_int()) {
        a++;
        b += (j - i);
        i += 2;
        if (i % 2 == 0) {
            j += 2;
        } else {
            j++;
        }
    }
    if (flag) {
        //@ assert(a == b);
    }
    return 0;
}
