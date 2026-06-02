// Source: A. Costan, S. Gaubert, E. Goubault, M. Martel, S. Putot: "A Policy
// Iteration Algorithm for Computing Fixed Points in Static Analysis of
// Programs", CAV 2005

#include "assert.h"

int main() {
    int i,j;
    i = 1;
    j = 10;
    /*@
    loop invariant j >= i ==> j >= 7;
    loop invariant j >= i ==> (i + 2*j) == 21;
    loop invariant i <= 2*j + 1;
    loop invariant i - j == 3*(10 - j) - 9;
    loop invariant 10 - j <= 9;
    loop invariant 0 <= 10 - j;
    loop invariant (j - 1) + (i - 1)/2 == 9;
    loop invariant j;
    loop invariant j >= i ==> (j - i) % 3 == 0;
    loop invariant j <= 10;
    loop invariant j <= 10 && j >= 0;
    loop invariant i >= 1 && i <= 21;
    loop invariant i == 1 + 2*(10 - j);
    loop invariant i <= 21;
    loop invariant i - 2*(10 - j) == 1;
    loop invariant i % 2 == 1;
    loop invariant 2*j + 1 <= i || j >= 1;
    loop invariant 1 <= j;
    loop invariant 1 <= j || 2*j + 1 <= i;
    loop invariant 1 <= i;
    loop invariant 1 < j;
    loop invariant 0 <= j;
    loop invariant (j >= i) ==> (i <= 15);
    loop invariant (j >= i) ==> ((j - i) % 3 == 0);
    loop invariant (j < i) ==> (j <= 6);
    loop invariant (i - 1) % 2 == 0;
    loop invariant (i + 2*j) == 21;
    loop invariant (10 - j) >= 0 ==> i == 1 + 2*(10 - j);
    loop invariant j>=6;
    loop assigns j;
    loop assigns i;
    */
    while (j >= i) {
        i = i + 2;
        j = -1 + j;
    }
    //@ assert(j == 6);
    return 0;
}
