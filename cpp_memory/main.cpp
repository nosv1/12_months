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
  auto p = std::make_shared<Tracer>();
  // 1
  std::cout << p.use_count() << ", " << p.get() << std::endl;
  {
    auto q = p;
    // 2
    std::cout << p.use_count() << std::endl;
  }
  // 2
  std::cout << p.use_count() << std::endl;
  auto r = std::move(p);
  // 2,
  std::cout << r.use_count() << ", " << p.get() << std::endl;
  std::cout << "resetting" << std::endl;
  r.reset();
  std::cout << "after reset" << std::endl;

  return 0;
}