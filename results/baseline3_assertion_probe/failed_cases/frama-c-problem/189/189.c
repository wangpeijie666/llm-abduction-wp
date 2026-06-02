int gcd(int a, int b) {
    /*@
        requires a >= 0 && b >= 0;
        assigns \nothing;
        ensures (a == 0) ==> \result == b;
        ensures (b == 0) ==> \result == a;
        ensures \result >= 0;
        ensures (a != 0 || b != 0) ==> \result > 0;
        ensures (a != 0) ==> (a % \result == 0);
        ensures (b != 0) ==> (b % \result == 0);
    */
    if (a == 0)
       return b;

    if (b == 0)
       return a;

    if (a == b)
        return a;

    if (a > b)
        return gcd(a-b, b);
    return gcd(a, b-a);
}

/*@
    ensures \result == 0;
*/
int main()
{
    int a = 98, b = 56;
    int c = gcd(a, b);
    //@ assert c == 14;
    return 0;
}
