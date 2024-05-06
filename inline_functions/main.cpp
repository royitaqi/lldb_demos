#include "foo.h"
#include "bar.h"

int g = 987;

int main() {
  foo_ret a = foo();
  bar_ret b = bar();
  int p = a.ret * 10 + b.ret; // 12 * 10 + 34 = 154
  int q = getFooRet() * 10 + getBarRet(); // 12 * 10 + 34 = 154
  return p - q + 23; // 23
}
