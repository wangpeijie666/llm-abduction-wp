// hhk2008_true-unreach-call.c

/*@
  requires \true;
  assigns \nothing;
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
      loop invariant 0 <= cnt; // Added to ensure cnt is non-negative
      loop assigns cnt, res;
      loop variant cnt;
    */
    while (cnt > 0) {
    	cnt = cnt - 1;
        res = res + 1;
    }

    //@ assert(res == a + b);
    
    return 0;
}
