int g = 987;

const char* const gs = "this is global";

int foo() {
  int i = 1;
  int j = 2;
  return i * 10 + j; // 12
}

int main() {
  int a = foo();
  int b = 3;
  const char* s = "hello world!";
  return a * 10 + b; // 123
}
