#include "foo.h"

int g = 987;

int main() {
  foo_ret a = foo();
  int b = 3;
  return a.ret * 10 + b; // 123
}
