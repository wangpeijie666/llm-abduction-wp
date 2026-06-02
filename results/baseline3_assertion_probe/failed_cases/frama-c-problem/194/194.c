int triangle(int a, int b, int c) {
    /*@
        assigns \nothing;
        ensures \result == 1 <==> ((a+b+c == 180) && a > 0 && b > 0 && c > 0);
        ensures \result == 0 <==> !((a+b+c == 180) && a > 0 && b > 0 && c > 0);
        ensures \result == 0 || \result == 1;
    */
    if ((a+b+c == 180) && a > 0 && b > 0 && c > 0) {
        return 1;
    } else {
        return 0;
    }
}

void check_validity() {
    /*@ assigns \nothing; */
    int res = triangle(90, 45, 45);
    //@ assert res == 1;
    res = triangle(90, 145, 145);
    //@ assert res == 0;
}
