#include <limits.h>
/*@
    assigns \nothing;
    ensures \result >= 0 && \result <= 10;
*/
int unknown_int();

/*@
    assigns \nothing;
    ensures \result >= 0 && \result < 2;
*/
int unknown_int1();

/*@
  assigns \nothing;
  ensures \result == 0;
*/
int main(int argc, char* argv[]) {
  int c1 = 4000;
  int c2 = 2000;
  int c3 = 10000;
  int n, v;
  int i, k, j;

  n = unknown_int();

  k = 0;
  i = 0;
  /*@
    loop invariant 0 <= i <= n;
    loop invariant k >= 0;
    loop invariant k >= 2000 * i;
    loop invariant 0 <= 2000 * i;
    loop invariant (v == 0 || v == 1) ==> k >= 0;
    loop invariant (i > 0) ==> (v == 0 || v == 1);
    loop invariant 0 <= k;
    loop invariant 2000 * i <= k;
    loop invariant 0 <= 2000 * i;
    loop assigns i, k, v;
  */
  /* PROBE_HERE:loop1_before */
  while( i < n ) {
    /* PROBE_HERE:loop1_body_entry */
    i++;
    v = unknown_int1();
    if( v == 0 )
      k += c1;
    else if( v == 1 )
      k += c2;
    else
      k += c3;
  }

  j = 0;
  /*@
    loop invariant 0 <= j <= n;
    loop invariant k >= 0;
    loop invariant j < n ==> k > 0;
    loop assigns j, k;
  */
  /* PROBE_HERE:loop2_before */
  while( j < n ) {
    /* PROBE_HERE:loop2_body_entry */
    //@ assert(k > 0);
    j++;
    k--;
  }

  return 0;
}
