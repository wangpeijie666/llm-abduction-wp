// hhk2008_true-unreach-call.c

/*@
  requires \true;
  ensures \result == 0;
*/
int main() {
    int a;
    int b;
    
    int res, cnt;

    res = a;
    cnt = b;
    
    /*@
      loop invariant cnt >= 0;
      loop invariant res == a + (b - cnt);
      loop assigns cnt, res;
      loop variant cnt;
    */
    /* PROBE_HERE:loop1_before */
    while (cnt > 0) {
    	/* PROBE_HERE:loop1_body_entry */
    	cnt = cnt - 1;
        res = res + 1;
    }

    //@ assert(res == a + b);
    
    return 0;
}
