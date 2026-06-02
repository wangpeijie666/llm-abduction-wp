// hhk2008_true-unreach-call.c
int main() {
    int a;
    int b;
    
    int res, cnt;

    res = a;
    cnt = b;
    
    /*@
      loop invariant cnt <= b;
      loop invariant res + cnt == a + b;
      loop invariant cnt > 0 ==> res + cnt == a + b;
      loop invariant cnt == b ==> res == a + (b - cnt);
      loop assigns cnt, res;
      loop invariant cnt <= 0 ==> res == a + b;
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
