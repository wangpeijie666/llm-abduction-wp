#include "assert.h"

int main() {
    int x = 1;
    int y = 0;
    /*@
      loop invariant 0 <= y <= 1000;
      loop invariant x >= 1;
      loop invariant x >= y;
      loop assigns x, y;
    */
    while (y < 1000) {
        x = x + y;
        y = y + 1;
    }
    //@ assert(x >= y);
    return 0;
}
