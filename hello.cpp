// ============================================================
// Welcome to your C++ IDE!
// Professor Del Valle — Coding Fundamentals
// ============================================================
// To compile and run:
//   Option A: Click the ▶ Run button (top right)
//   Option B: Open Terminal and type:
//             g++ -std=c++17 -o hello hello.cpp && ./hello
// ============================================================

#include <iostream>
#include <string>

int main() {
    std::string name;
    std::cout << "Enter your name: ";
    std::getline(std::cin, name);
    std::cout << "Hello, " << name << "! Welcome to C++17.\n";
    return 0;
}
