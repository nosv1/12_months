#ifndef IMU_READING_H

#define IMU_READING_H

#include <string>

#include "timestamp.h"

struct Acceleration {
  double x_mps2;
  double y_mps2;
  double z_mps2;  // at rest z = +9.81
  explicit Acceleration(double x_mps2, double y_mps2, double z_mps2)
      : x_mps2(x_mps2), y_mps2(y_mps2), z_mps2(z_mps2) {}
  std::string to_string();
};

struct Gyro {
  double x_rad_s;
  double y_rad_s;
  double z_rad_s;
  explicit Gyro(double x_rad_s, double y_rad_s, double z_rad_s)
      : x_rad_s(x_rad_s), y_rad_s(y_rad_s), z_rad_s(z_rad_s) {}
  std::string to_string();
};

struct IMUReading {
  Timestamp timestamp;  // high res clock duration (needs testing to know what this outputs)
  Acceleration accel;   // m/s^2
  Gyro gyro;            // rad/s
  explicit IMUReading(Timestamp timestamp, Acceleration accel, Gyro gyro)
      : timestamp(timestamp), accel(accel), gyro(gyro) {}
  std::string to_string();
};

#endif