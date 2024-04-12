#include "foo.h"

int main() {
  Foo foo;
  int a = foo.GetValue();
  int b = Foo::GetStaticValue();
  return a * 10 + b; // 123
}
