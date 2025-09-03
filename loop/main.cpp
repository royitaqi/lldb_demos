#include <iostream>

int main() {
    int a = 0;
    int b = 0;
    for (;;) {
	for (int i = 0; i < 100000000; i++) {
            b++;
        }
	std::cout << a++ << "            \r";
        std::cout.flush();
    }
    return 0;
}
