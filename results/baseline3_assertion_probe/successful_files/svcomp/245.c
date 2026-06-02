#include <limits.h>
/*@
    ensures \result > 0 && \result <= INT_MAX;
    assigns \nothing;
*/
int unknown_int();

/*@
  assigns \nothing;
*/
int main() {
  int i,k,n,l;

  n = unknown_int();
  l = unknown_int();
  /*@
    loop invariant 1 <= k <= n;
    loop invariant 1 <= l;
    loop assigns k, l, i;
  */
  /* PROBE_HERE:loop1_before */
  for (k=1;k<n;k++){
    /* PROBE_HERE:loop1_body_entry */
    /*@
      loop invariant l <= i;
      loop invariant 1 <= i;
      loop invariant 1 <= l;
      loop assigns i;
    */
    /* PROBE_HERE:loop2_before */
    for (i=l;i<n;i++){  
      /* PROBE_HERE:loop2_body_entry */
      //@ assert 1<=i;
    }
    if(unknown_int())
      l = l + 1;
  }
 }
