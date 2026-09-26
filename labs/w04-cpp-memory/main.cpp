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

Tracer make_tracer() {
  // ctor
  Tracer t;
  std::cout << "&t = " << &t << std::endl;
  return t;
}
// dtor

int main() {
  Tracer u = make_tracer();
  std::cout << "&u = " << &u << std::endl;
  // move
  return 0;
}