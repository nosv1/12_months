#ifndef TIMESTAMP_H

#define TIMESTAMP_H

#include <chrono>

struct Timestamp {
  std::chrono::time_point<std::chrono::steady_clock> v;
  Timestamp(std::chrono::time_point<std::chrono::steady_clock> timestamp) : v(timestamp) {}
};

#endif