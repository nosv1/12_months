#include "timestamp.h"

#include <sstream>
#include <string>

std::string Timestamp::to_string() {
  auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(this->v);
  std::ostringstream oss;
  oss << ms.count() << " ms";
  return oss.str();
}