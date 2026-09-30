#include "imu_reading.h"

#include <sstream>
#include <string>

// ACCELERATION

bool Acceleration::operator==(const Acceleration& other) const {
  return this->x_mps2 == other.x_mps2 && this->y_mps2 == other.y_mps2 &&
         this->z_mps2 == other.z_mps2;
}

std::string Acceleration::to_string() const {
  std::ostringstream oss;
  oss << "accel (x, y, z) mps2: (" << this->x_mps2;
  oss << ", " << this->y_mps2;
  oss << ", " << this->z_mps2;
  oss << ")";
  return oss.str();
}

// GYRO

bool Gyro::operator==(const Gyro& other) const {
  return this->x_rad_s == other.x_rad_s && this->y_rad_s == other.y_rad_s &&
         this->z_rad_s == other.z_rad_s;
}

std::string Gyro::to_string() const {
  std::ostringstream oss;
  oss << "gyro (x, y, z) rad/s: (" << this->x_rad_s;
  oss << ", " << this->y_rad_s;
  oss << ", " << this->z_rad_s;
  oss << ")";
  return oss.str();
}

// IMU READING

bool IMUReading::operator==(const IMUReading& other) const {
  return this->timestamp == other.timestamp && this->accel == other.accel &&
         this->gyro == other.gyro;
}

std::string IMUReading::to_string() const {
  std::ostringstream oss;
  oss << "timestamp: " << this->timestamp.to_string() << std::endl;
  oss << this->accel.to_string() << std::endl;
  oss << this->gyro.to_string();
  return oss.str();
}

std::ostream& operator<<(std::ostream& os, const IMUReading& r) { return os << r.to_string(); };
