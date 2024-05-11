#include "foo.h"
#include "bar.h"
#include "not_inline.h"

int main() {
  int f = get_foo_ret(); // 12
  int b = get_bar_ret(); // 34
  int s = get_value_not_inlined(); // 22
  return b - f - s; // 0
}
