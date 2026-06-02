int unknown1();
int unknown2();

/*@
  assigns \nothing;
*/
int unknown1();
/*@
  assigns \nothing;
*/
int unknown2();


/*@
  assigns \nothing;
*/
int main(int flag)
{
  int t = 0;
  int s = 0;
  int a = 0;
  int b = 0;
  /*@
    loop invariant a == b;
    loop invariant (flag == 0 ==> s == t) && (flag != 0 ==> t == 2*s);
    loop invariant flag == 0 ==> s == t;
    loop assigns a, b, s, t;
  */
  /* PROBE_HERE:loop1_before */
  while(unknown1()) {
    /* PROBE_HERE:loop1_body_entry */
    a++;
    b++;
    s += a;
    t += b;
    if(flag) {
      t += a;
    }
  } 
  //2s >= t
  int x = 1;
  if(flag) {
    x = t - 2*s + 2;
  }
  //x <= 2
  int y = 0;
  // invariant (x <= 2 && y <= x + 2)
  /*@
    loop invariant x <= 2;
    loop invariant y <= x + 2;
    loop assigns y;
  */
  /* PROBE_HERE:loop2_before */
  while(y <= x){
    /* PROBE_HERE:loop2_body_entry */
    if(unknown2()) 
       y++;
    else 
       y += 2;
  }
  //@ assert(y <= 4);
}
