class Foo {
public:
  static int static_foo() {
    int i = 1;
    int j = 2;
    return i * 10 + j; // 12
  }

  int foo() {
    int p = 3;
    int q = 4;
    return p * 10 + q; // 34
  }
};
