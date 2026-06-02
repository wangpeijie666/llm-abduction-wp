int main(){

    int x = 0;
    int y = 0;

    /*@
      loop invariant y >= 0;
      loop assigns y;
    */
    /* PROBE_HERE:loop1_before */
    while(y >= 0){
        /* PROBE_HERE:loop1_body_entry */
        y = y + x;
    }

    //post-condition
    //@ assert( y >= 0);
}
