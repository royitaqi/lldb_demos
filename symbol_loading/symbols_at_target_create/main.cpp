int foo() {
  int i = 1;
  int j = 2;
  return i * 10 + j; // first breakpoint
}

int bar() {
  int k = 3;
  int l = 4;
  return k * 10 + l; // second breakpoint
}

int main() {
  int a = foo();
  int b = bar();
  return a + b - 46; // 0
}
