int g = 987;

const char* const gs = "this is global";

int foo() {
  int i = 1;
  int j = 2;
  return i * 10 + j; // 12
}

int main(int argc, char** argv) {
  bool wait = false;
  for (int i = 1; i < argc; i++) {
    if (argv[i][0] == '-' && argv[i][1] == 'w' && argv[i][2] == 0) {
      wait = true;
    }
  }

  while (wait) {
    // do nothing
  }

  int a = foo();
  int b = 3;
  const char* s = "hello world!";
  return a * 10 + b; // 123
}
