/*@
  requires n >= 0;
  ensures \result == n;
*/
void foo(int n) {
  int x = n;
  int y = 0;

  /*@
    loop invariant 0 <= x <= n;
    loop invariant 0 <= y <= n;
    loop invariant x + y == n;
    loop assigns x, y;
  */
  while (x > 0) {
    x--;
    y++;
  }

  //@ assert y == n;
}
