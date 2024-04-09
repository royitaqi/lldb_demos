#include "foo.h"

foo_ret foo() {
  int i = 1;
  int j = 2;
  return foo_ret { i * 10 + j }; // 12
}
