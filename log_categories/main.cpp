#include "foo.h"

int g = 987;

int main() {
  foo_ret a = foo();
  return a.ret * 10 + 3; // 12 * 10 + 3 = 123
}
