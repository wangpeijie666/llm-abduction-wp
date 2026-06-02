int main(){
    int i=0;

    /*@
      loop invariant 0 <= i <= 30;
      loop assigns i;
    */
    /* PROBE_HERE:loop1_before */
    while (i<30){
        /* PROBE_HERE:loop1_body_entry */
        ++i;
    }
    //@ assert i==30;
   
}
