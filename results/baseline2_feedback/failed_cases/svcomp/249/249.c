// sum01_true-unreach-call_true-termination.c

/*@
  requires n >= 0;
  assigns i, sn;
  ensures sn == n * 2 || sn == 0;
*/
int main() {
    int n;
    int i = 0;
    int sn = 0;

    /*@
      loop invariant 1 <= i <= n + 1;
      loop invariant sn == (i - 1) * 2;
      loop assigns i, sn;
      loop variant n - i + 1;
    */
    for (i = 1; i <= n; i++) {
        sn = sn + 2;
    }

    //@ assert(sn == n * 2 || sn == 0);

    return 0;
}
