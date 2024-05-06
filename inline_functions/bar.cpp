#include "bar.h"

#include "inline_in_source.cpp"

bar_ret bar() {
  int i = 3;
  int j = 4;
  return bar_ret { i * 10 + j }; // 34
}

int getBarRet() {
  return getRetInSource<>(bar());
}
