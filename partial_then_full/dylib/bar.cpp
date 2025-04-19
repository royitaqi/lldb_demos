#include "bar.h"

bar_ret bar() {
  int i = 3;
  int j = 4;
  return bar_ret { i * 10 + j }; // 34
}
