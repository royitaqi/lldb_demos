#include <thread>

void funcA() {
  int a = 1;
  int aa = 2;
  int aaa = 3;
}

void funcB() {
  int b = 1;
  int bb = 2;
  int bbb = 3;
}

void funcC() {
  int c = 1;
  int cc = 2;
  int ccc = 3;
}

int main() {
  auto tA = std::thread(funcA);
  auto tB = std::thread(funcB);
  auto tC = std::thread(funcC);

  tA.join();
  tB.join();
  tC.join();
  return 0;
}
