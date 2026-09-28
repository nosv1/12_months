#include "timestamp.h"

#include <sstream>
#include <string>

bool Timestamp::operator==(const Timestamp& other) const { return this->v == other.v; }

std::string Timestamp::to_string() const {
  auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(this->v);
  std::ostringstream oss;
  oss << ms.count() << " ms";
  return oss.str();
}