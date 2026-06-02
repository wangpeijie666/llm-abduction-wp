/*@
  assigns \nothing;
  ensures \result == (base * height) / 2;
*/
int area(int base, int height){
    int res = (base *  height)/2;
    return res;
}

/*@
  ensures \result == 0;
*/
int main() {
    int a = area(4, 5);
    //@ assert a == 10;
    return 0;
}
