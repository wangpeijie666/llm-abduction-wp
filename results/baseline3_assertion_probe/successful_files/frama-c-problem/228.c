/*@ 
  requires \valid_read(a);
  requires \valid_read(b);
  assigns \nothing;
  ensures \result == *a || \result == *b;
  ensures \result >= *a && \result >= *b;
  ensures (*a < *b) ==> \result == *b;
  ensures (*a >= *b) ==> \result == *a;
*/
int max_ptr(int *a, int *b){
    return (*a < *b) ? *b : *a ;
}

extern int h;

/*@
  assigns h;
*/
int main() {
    h = 42;
    int a = 24;
    int b = 42;

    int x = max_ptr(&a, &b);

    //@ assert x == 42;
    //@ assert h == 42;
}
