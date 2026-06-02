/*@ requires \valid(q) && \valid(r);
    requires y != 0;
    assigns *q, *r;
    ensures *q == (unsigned)(x / y);
    ensures *r == (unsigned)(x % y);
    ensures \old(q) == q && \old(r) == r;
*/
void div_rem(unsigned x, unsigned y, unsigned* q, unsigned* r) {
    *q = x / y;
    *r = x % y;
}

// write a test
void main() {
    unsigned q, r;
    div_rem(10, 3, &q, &r);
    //@ assert q == 3;
    //@ assert r == 1;
}
