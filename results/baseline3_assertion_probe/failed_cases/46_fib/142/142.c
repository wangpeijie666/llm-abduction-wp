#include <assert.h>

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();
/*@ assigns \nothing; */
int unknown3();

/*
 * "fragtest_simple" from InvGen benchmark suite
 */

/*@ ensures \result == 0; */
int main(){
  int i, pvlen;
  int t;
  int k = 0;
  int n;
  i = 0;

  //  pkt = pktq->tqh_first;
  /*@
    loop invariant i >= 0;
    loop assigns i;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown1())
    i = i + 1;
  
  if (i > pvlen) {
      /* PROBE_HERE:loop1_body_entry */
    pvlen = i;
  } else {

  }
  i = 0;

  /*@
    loop invariant i >= 0;
    loop invariant k >= 0;
    loop invariant k == i;
    loop assigns t, i, k;
  */
  /* PROBE_HERE:loop2_before */
  while (unknown2()) {
    /* PROBE_HERE:loop2_body_entry */
    t = i;
    i = i + 1;
    k = k + 1;
  }
  /*@
    loop assigns \nothing;
  */
  /* PROBE_HERE:loop3_before */
  while (unknown3());

  int j = 0;
  n = i;
  /*@
    loop invariant n == \at(i,Pre) + j;
    loop invariant 0 <= j <= n;
    loop invariant i == n - j;
    loop invariant k == i;
    loop invariant k >= 0;
    loop assigns k, i, j;
  */
  /* PROBE_HERE:loop4_before */
  while (1) {
    /* PROBE_HERE:loop4_body_entry */
    //@ assert(k >= 0);
    k = k - 1;
    i = i - 1;
    j = j + 1;
    if (j < n) {
      /* PROBE_HERE:loop3_body_entry */
    } else {
      break;
    }
  }
  return 0;
}
