/*@ 
    requires \valid(a);
    requires \valid_read(b);
    assigns *a;
    ensures (\old(*b) != 0) ==> *a == 0;
    ensures (\old(*b) == 0) ==> *a == \old(*a);
    ensures *b == \old(*b);
*/
void reset_1st_if_2nd_is_true(int* a, int const* b){
    /*@
        requires \valid(a);
        requires \valid_read(b);
        assigns *a;
        ensures (\old(*b) != 0) ==> *a == 0;
        ensures (\old(*b) == 0) ==> *a == \old(*a);
    */
    if(*b) *a = 0 ;
}

int main(){
    /*@ assigns \nothing; */
    int a = 5 ;
    int x = 0 ;
    reset_1st_if_2nd_is_true(&a, &x);
    //@ assert a == 5 ;
    //@ assert x == 0 ;

    int const b = 1 ;
    reset_1st_if_2nd_is_true(&a, &b);
    //@ assert a == 0 ;
    //@ assert b == 1 ;
}
