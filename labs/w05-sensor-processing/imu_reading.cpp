#include "imu_reading.h"

#include <sstream>
#include <string>

std::string IMUReading::to_string() {
  std::ostringstream oss;
  oss << "timestamp: " << this->timestamp.to_string();
  return oss.str();
}