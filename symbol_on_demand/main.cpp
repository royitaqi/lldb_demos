int g = 987;

struct foo_ret {
  int ret;
};

foo_ret foo() {
  int i = 1;
  int j = 2;
  return foo_ret { i * 10 + j }; // 12
}

int main() {
  foo_ret a = foo();
  int b = 3;
  return a.ret * 10 + b; // 123
}
