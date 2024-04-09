#include "foo.h"

int g = 987;

int main() {
  int a = foo();
  int b = 3;
  return a * 10 + b; // 123
}
