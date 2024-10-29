#include "foo.h"

int main() {
  foo_ret a = foo();
  return a.ret; // 12
}
