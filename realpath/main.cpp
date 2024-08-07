#include "symlink1/foo.h"
#include "symlink2/bar.h"
#include "symlink2/qux.h"

int main() {
  int a = foo(); // 12
  int b = bar(); // 34
  int c = qux(); // 56
  return a + b + c; // 102
}
