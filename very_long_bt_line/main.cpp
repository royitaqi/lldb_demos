#include <vector>

int g = 987;

int foo(const std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>> &bar) {
  int i = 1;
  int j = 2;
  return i * 10 + j;
}

int main() {
  auto v = std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>();
  int a = foo(v);
  int b = 3;
  return a * 10 + b; // 123
}
