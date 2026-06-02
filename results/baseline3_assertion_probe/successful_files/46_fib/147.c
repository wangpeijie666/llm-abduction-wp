#include <assert.h>
int unknown1();
int unknown2();
int unknown3();
int unknown4();

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
int unknown3();
/*@ 
  assigns \nothing;
*/
int unknown4();


/*@
  assigns \nothing;
*/
int main() {
  int a = 0;
  int j;
  int m;
  if(m<=0)
    return 0;
  /*@
    loop invariant 1 <= j <= m+1;
    loop invariant -(j-1) <= a <= (j-1);
    loop assigns j, a;
  */
  /* PROBE_HERE:loop1_before */
  for(j = 1; j <= m ; j++){
    /* PROBE_HERE:loop1_body_entry */
    if(unknown1()) 
       a++;
    else
       a--; 
  }
  //@ assert(a>=-m);
  //@ assert(a<=m);
}
