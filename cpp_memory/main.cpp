#include <iostream>
#include <memory>
#include <stdexcept>
#include <vector>

struct T {
  int* t;
  T(int* t) : t(t) {}
  ~T() { delete t; }
  T(const T&) = delete;
};

int make_and_delete_int() {
  auto t = std::make_unique<int>(1);
  // auto u = t;
  throw std::runtime_error("eee");
  return 0;
}

struct Tracer {
  Tracer() { std::cout << "ctor" << std::endl; };
  Tracer(const Tracer& other) { std::cout << "copy" << std::endl; };
  Tracer(Tracer&& other) { std::cout << "move" << std::endl; };
  ~Tracer() { std::cout << "dtor" << std::endl; }
};

int main() {
  // borrowed int pointer
  int* borrowed;
  {
    // unique pointer, p to int
    std::unique_ptr<int> p(new int(7));
    // p.get() is the address
    borrowed = p.get();
    // borrowed is now the address of p's int
    // p's address gets deconstructed, so the address is freed,
  }
  // get the value at borrowed's address
  std::cout << "*borrowed = " << *borrowed;
  return 0;
}