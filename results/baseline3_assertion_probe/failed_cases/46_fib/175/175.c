int unknown1();
int unknown2();

/*@ assigns \nothing; */
int unknown1();
/*@ assigns \nothing; */
int unknown2();

/*@
  assigns \nothing;
*/
void foo(int flag) {
  int x = 1;
  int y = 1;
  int a;

  if (flag)
    a = 0;
  else
    a = 1;

  /*@
    loop invariant x >= 1;
    loop invariant x > 0;
    loop invariant y >= 1;
    loop invariant x == y;
    loop invariant (flag != 0 ==> x == y + 2*(a/2));
    loop invariant (flag == 0 ==> y == x + 2*(a/2));
    loop invariant (flag != 0 ==> a % 2 == 0);
    loop invariant (flag == 0 ==> a % 2 == 1);
    loop assigns x, y, a;
  */
  /* PROBE_HERE:loop1_before */
  while (unknown1()) {
    /* PROBE_HERE:loop1_body_entry */
    if (flag) {
      a = x + y;
      x++;
    } else {
      a = x + y + 1;
      y++;
    }
    if (a % 2 == 1)
      y++;
    else
      x++;
  }
  //x==y

  if (flag)
    a++;
  //@ assert(a % 2 == 1);
}
