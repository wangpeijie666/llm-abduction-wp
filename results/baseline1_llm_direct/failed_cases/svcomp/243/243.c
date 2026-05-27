#include <limits.h>

int main() {
    int i;
    int j;

    int x = i;
    int y = j;
    /*@
      loop invariant x >= 0;
      loop invariant y <= j;
      loop invariant y == j - (i - x);
      loop assigns x, y;
    */
    while (x != 0) {
        x--;
        y--;
    }

    if (i == j) {
        //@ assert y == 0;
    }
    
    return 0;
}
