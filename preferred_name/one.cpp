template <typename T> struct Foo;

typedef Foo<int> BarInt;

template <typename T>
struct [[clang::preferred_name(BarInt)]] Foo{};

int main() {
  BarInt barInt;
  return 0;
}
