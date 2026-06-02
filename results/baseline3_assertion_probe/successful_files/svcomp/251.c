#include <limits.h>
/*@
ensures INT_MIN <= \result <= INT_MAX;
assigns \nothing;
*/
int unknown_int();

/*@
assigns \nothing;
*/
int main() {
  int n;
  int i = 0;
  int k = 0;
  n = unknown_int();
  /*@
    loop invariant 0 <= i;
    loop invariant k == i;
    loop assigns i, k;
  */
  /* PROBE_HERE:loop1_before */
  while( i < n ) {
	  /* PROBE_HERE:loop1_body_entry */
	  i++;
	  k++;
  }

  int j = 0;
  /*@
    loop invariant 0 <= j;
    loop invariant k == i - j;
    loop assigns j, k;
  */
  /* PROBE_HERE:loop2_before */
  while( j < n ) {
    /* PROBE_HERE:loop2_body_entry */
    //@ assert (k > 0);
    j++;
    k--;
  }
}
