#include <limits.h>

/*@
  assigns \nothing;
  behavior nonneg:
    assumes val >= 0;
    ensures \result == val;
  behavior neg:
    assumes val < 0;
    ensures val == INT_MIN ? \result == INT_MIN : \result == -val;
  complete behaviors nonneg, neg;
  disjoint behaviors nonneg, neg;
*/
int abs(int val) {
    if(val < 0) return -val;
    return val;
}

/*@ assigns \nothing; */
void foo(int a) {
    int b = abs(-42);
    //@ assert b == 42;
    int c = abs(42);
    //@ assert c == 42;
    int d = abs(a);
    int e = abs(INT_MIN);
}
