#include <limits.h>

/*@
  ensures INT_MIN <= \result <= INT_MAX;
*/
int unknown_int();

int main() {
    int a;
    int b;
    
    int res, cnt;

    res = a;
    cnt = b;
    
    /*@
      loop invariant cnt >= 0;
      loop invariant res == a + (b - cnt);
      loop assigns cnt, res;
    */
    while (cnt > 0) {
        cnt = cnt - 1;
        res = res + 1;
    }

    //@ assert(res == a + b);
    
    return 0;
}
