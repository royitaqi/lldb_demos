#include "foo.h"
#include "bar.h"

int g = 987;

int main() {
  foo_ret a = foo();
  bar_ret b = bar();
  return a.ret * 10 + b.ret; // 12 * 10 + 34 = 154
}
