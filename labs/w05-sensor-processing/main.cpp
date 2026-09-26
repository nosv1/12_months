#include <chrono>

#include "imu_reading.h"
#include "timestamp.h"

int main() {
  IMUReading r(Timestamp(std::chrono::steady_clock::now()), Acceleration(1, 1, 1), Gyro(1, 1, 1));
  return 0;
}