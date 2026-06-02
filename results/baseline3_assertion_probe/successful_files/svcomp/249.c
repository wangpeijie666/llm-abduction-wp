// sum01_true-unreach-call_true-termination.c
/*@ 
  assigns \nothing;
*/
int main() {
    int n;
    int i=0;
    int sn=0;
    
    /*@
      loop invariant 1 <= i;
      loop invariant (n < 0) ==> (i == 1);
      loop invariant (0 <= n) ==> (i <= n+1);
      loop invariant sn == (i-1) * 2;
      loop assigns i, sn;
    */
    /* PROBE_HERE:loop1_before */
    for (i = 1; i <= n; i++) {
        /* PROBE_HERE:loop1_body_entry */
        sn = sn + (2);
    }
    
    //@ assert(sn == n * (2) || sn == 0);
    
    return 0;
}
