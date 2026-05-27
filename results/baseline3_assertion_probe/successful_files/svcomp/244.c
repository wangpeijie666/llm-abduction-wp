#include <limits.h>
/*@
    ensures \result >= 0 && \result <= 10;
    assigns \nothing;
*/
int unknown_int();

/*@
    ensures \result >= 0 && \result < 2;
    assigns \nothing;
*/
int unknown_int1();

int main(int argc, char* argv[]) {
  int c1 = 4000;
  int c2 = 2000;
  int c3 = 10000;
  int n, v;
  int i, k, j;

  /*@
    assigns n;
    ensures n >= 0 && n <= 10;
  */
  n = unknown_int();

  k = 0;
  i = 0;
  /*@
    loop invariant 0 <= i <= n && i <= k;
    loop invariant k >= 0;
    loop assigns i, k, v;
    loop variant n - i;
  */
  /* PROBE_HERE:loop1_before */
  while( i < n ) {
    /* PROBE_HERE:loop1_body_entry */
    i++;
    /*@
      assigns v;
      ensures v >= 0 && v < 2;
    */
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
    loop invariant k >= n - j;
    loop assigns j, k;
    loop variant n - j;
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
