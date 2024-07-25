int foo() {
  int i = 1;
  int j = 2;
  return i * 10 + j; // 12
}

int main() {
  int a = foo();
  int b = 3;
  return a * 10 + b; // 123
}
