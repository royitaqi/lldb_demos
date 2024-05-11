#include "foo.h"

#include "inline_for_foo.h"

foo_ret foo() {
  int i = 1;
  int j = 2;
  return foo_ret { i * 10 + j }; // 12
}

int get_foo_ret() {
  int a = get_foo_ret_inlined(foo());
  return a; // 12
}
