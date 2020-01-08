
//! Basic no usage
int foo(void) {
    int foobish = 1;
    return foobish;
}

//! Prevent tripping on veneer symbol names
int ____aeabi_d2f_veneer(void) {
    volatile int heyo = 7;
    return heyo;
}
