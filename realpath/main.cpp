#include "symlink/foo.h"
#include "symlink/bar.h"

int main() {
  int a = foo(); // 12
  int b = bar(); // 34
  return a + b; // 46
}
