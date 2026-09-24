#include <iostream>
#include <memory>
#include <stdexcept>

struct T {
  int* t;
  T(int* t) : t(t) {}
  ~T() { delete t; }
  T(const T&) = delete;
};

int make_and_delete_int() {
  auto t = std::make_unique<int>(1);
  auto u = t;
  throw std::runtime_error("eee");
  return 0;
}

int main() {
  try {
    make_and_delete_int();
  } catch (const std::runtime_error& e) {
  };
  return 0;
}