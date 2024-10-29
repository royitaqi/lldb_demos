int main() {
    int a = 10;
    bool f = true;
    for (;;) {
        if (f) {
            a += 2;
        } else {
            a -= 2;
        }
        f = !f;
    }
    return 0;
}
