#include <stdio.h>

/*@ 
  // External functions used by pdt.
  // No strong guarantees are assumed; only frame conditions.
  assigns \nothing;
*/
int power(int x);

/*@ 
  assigns \nothing;
*/
int factorial(int x);

/*@
  assigns \nothing;
*/
int pdt(int n) {
  int prod = 1;
  int i = 2;

  /*@
    loop invariant 2 <= i;
    loop invariant \exists integer k; i == 2*k;
    loop invariant \true;
    loop assigns prod, i;
  */
  /* PROBE_HERE:loop1_before */
  while(i < n) {
    /* PROBE_HERE:loop1_body_entry */
    prod = power(i/2)*factorial(i/2);
    i = i+2;
  }
  return prod;
}

/*@
  assigns \nothing;
*/
int main() {
    int p = pdt(10);
    //@ assert p == 1;
}
