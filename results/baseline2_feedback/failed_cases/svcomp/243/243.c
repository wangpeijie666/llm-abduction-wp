int main() {
    int i;
    int j;

    int x = i;
    int y = j;

    /*@
      loop invariant x >= 0;
      loop invariant y == j - (i - x);
      loop invariant x <= i;
      loop assigns x, y;
      loop variant x;
    */
    while (x != 0) {
        x--;
        y--;
    }

    if (i == j) {
        //@ assert(y == 0);
    }

    return 0;
}
