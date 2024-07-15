#include "foo.h"

int main() {
  int a = Foo::static_foo(); // 12

  Foo foo;
  int b = foo.foo(); // 34
  
  return a + b; // 46
}
