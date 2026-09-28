#ifndef TIMESTAMP_H

#define TIMESTAMP_H

#include <chrono>
#include <string>

struct Timestamp {
  std::chrono::steady_clock::duration v;
  explicit Timestamp(std::chrono::steady_clock::duration timestamp) : v(timestamp) {}
  bool operator==(const Timestamp& other) const;
  std::string to_string() const;
};

#endif