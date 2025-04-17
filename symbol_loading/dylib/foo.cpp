#include "foo.h"

#include "bar.h"

int foo() {
  int b = bar(); // 2
  return 10 + b; // 12
}
