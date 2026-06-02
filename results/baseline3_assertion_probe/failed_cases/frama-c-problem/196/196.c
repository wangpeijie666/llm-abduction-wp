/*@
  requires -5 <= x <= 5;
  requires -20 <= y <= 5;
  assigns \nothing;
  ensures \result == (x - 5) + (y + 10);
*/
int function(int x, int y) {
    int res ;
    y += 10 ;
    x -= 5 ;
    res = x + y ;
    //@ assert -15 <= res <= 5;
    return res ;
}

// write a test
/*@
  assigns \nothing;
*/
void main() {
    int t = function(-5, 5);
    //@ assert t == 5;
}
