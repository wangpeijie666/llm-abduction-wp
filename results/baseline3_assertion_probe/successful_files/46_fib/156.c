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
 * ex49 from NECLA Static Analysis Benchmarks
 */
/*@
requires n >= 0;
assigns \nothing;
ensures \true;
*/
void foo(int n) {
  int i, sum = 0;

  /*@
    loop invariant 0 <= i <= n;
    loop invariant sum >= 0;
    loop invariant sum == i*(i-1)/2;
    loop assigns i, sum;
  */
  /* PROBE_HERE:loop1_before */
  for (i = 0; i < n; ++i)
    sum = sum + i;

  //@ assert(sum >= 0);
}
