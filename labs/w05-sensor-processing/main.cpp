#include <chrono>
#include <iostream>

#include "imu_buffer.h"
#include "imu_reading.h"
#include "timestamp.h"

int main() {
  IMUReading r{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(1, 1, 1), Gyro(1, 1, 1)};

  IMUReading s{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(2, 1, 1), Gyro(1, 1, 1)};

  IMUReading t{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(3, 1, 1), Gyro(1, 1, 1)};

  IMUReading u{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(4, 1, 1), Gyro(1, 1, 1)};

  const std::size_t imu_buffer_size = 3;
  IMUBuffer imu_buffer(imu_buffer_size);
  imu_buffer.add_readings({r, s, t});
  imu_buffer.add_readings({u});

  return 0;
}