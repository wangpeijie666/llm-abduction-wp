#include <stdio.h>

/*@
  requires 0 <= n;
  assigns \nothing;
  ensures \result >= 1;
  ensures n > 0 ==> \result >= 1;
  ensures (n > 0) ==> (\result >= 1);
  ensures n == 5 ==> \result == 120;
*/
int factorial(int n) {

  int i = 1;
  int f = 1;

  /*@
    loop invariant 1 <= i <= n+1;
    loop invariant f >= 1;
    loop invariant n == 5 ==> ((i==1 && f==1) || (i==2 && f==1) || (i==3 && f==2) || (i==4 && f==6) || (i==5 && f==24) || (i==6 && f==120));
    loop assigns i, f;
  */
  /* PROBE_HERE:loop1_before */
  while (i <= n)  {
    /* PROBE_HERE:loop1_body_entry */
    f = f * i;
    i = i + 1;
  }
  return f;
}

// write a test
/*@
  assigns \nothing;
*/
void main() {
  int t = factorial(5);
  //@ assert t == 120;
}
