#include "imu_reading.h"

#include <sstream>
#include <string>

std::string Acceleration::to_string() {
  std::ostringstream oss;
  oss << "accel (x, y, z) mps2: (" << this->x_mps2;
  oss << ", " << this->y_mps2;
  oss << ", " << this->z_mps2;
  oss << ")";
  return oss.str();
}

std::string Gyro::to_string() {
  std::ostringstream oss;
  oss << "gyro (x, y, z) rad/s: (" << this->x_rad_s;
  oss << ", " << this->y_rad_s;
  oss << ", " << this->z_rad_s;
  oss << ")";
  return oss.str();
}

std::string IMUReading::to_string() {
  std::ostringstream oss;
  oss << "timestamp: " << this->timestamp.to_string() << std::endl;
  oss << this->accel.to_string() << std::endl;
  oss << this->gyro.to_string();
  return oss.str();
}