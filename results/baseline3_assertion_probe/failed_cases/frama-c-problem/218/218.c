int check(int *a, int *b, int n) {
    /*@
        requires n >= 0;
        requires \valid_read(a + (0..n-1));
        requires \valid_read(b + (0..n-1));
        assigns \nothing;
        ensures \result == 0 || \result == 1;
        ensures \result == 1 <==> (\forall integer i; 0 <= i < n ==> a[i] == b[i]);
    */
    /* PROBE_HERE:loop1_before */
    for (int i = 0; i < n; i++) {
        /* PROBE_HERE:loop1_body_entry */
        if (a[i] != b[i]) {
            return 0;
        }
    }
    return 1;
}

int main() {
    int a[] = {1,2,3,4,5};
    int b[] = {1,2,3,4,5};
    int res = check(a, b, 5);
    //@ assert res == 1;
}
