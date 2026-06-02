#include <assert.h>

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();
/*@ assigns \nothing; */
int unknown3();
/*@ assigns \nothing; */
int unknown4();

/*
 * Taken from "Counterexample Driven Refinement for Abstract Interpretation" (TACAS'06) by Gulavani
 */
/*@
requires n > 0;
assigns \nothing;
*/
void foo(int n) {
  int x = 0;
  int m = 0;
  /*@
    loop invariant 0 <= x <= n;
    loop invariant 0 <= m <= x;
    loop invariant x <= n;
    loop invariant 0 <= x;
    loop invariant 0 <= m;
    loop invariant (x > 0 ==> m < x);
    loop assigns x, m;
  */
  /* PROBE_HERE:loop1_before */
  while (x < n) {
    /* PROBE_HERE:loop1_body_entry */
    if (unknown1()) {
      m = x;
    }
    x = x + 1;
  }
  if (n > 0) {
    //@ assert(0 <= m && m < n);
  }
}
