/*@ 
  assigns \nothing;
  behavior a_zero:
    assumes a == 0;
    ensures \result == 0;
  behavior a_nonzero:
    assumes a != 0;
    ensures \result == 1;
  complete behaviors a_zero, a_nonzero;
  disjoint behaviors a_zero, a_nonzero;
*/
int func(int a) {
    int x, y;
    int sum, res;
    if (a == 0){
        x = 0; y = 0;
    }
    else {
        x = 5; y = 5;
    }
    sum = x + y; 
    /*@ assert (a == 0 ==> sum == 0) && (a != 0 ==> sum == 10); */
    /*@ assert a != 0 ==> sum != 0; */
    res = 10/sum; 
    return res;
}

/*@ ensures \result == 0; */
int main() {
    int a = func(4);
    //@ assert a == 1;
    return 0;
}
