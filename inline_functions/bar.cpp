#include "bar.h"

#include "inline_for_bar.cpp"

bar_ret bar() {
  int i = 3;
  int j = 4;
  return bar_ret { i * 10 + j }; // 34
}

int get_bar_ret() {
  int a = get_bar_ret_inlined(bar());
  return a; // 34
}
