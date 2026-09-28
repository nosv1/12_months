#include <gtest/gtest.h>

#include "imu_buffer.h"
#include "imu_reading.h"
#include "timestamp.h"

TEST(SensorProcessing, IMUBufferOrderTest) {
  IMUReading r{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(1, 1, 1), Gyro(1, 1, 1)};

  IMUReading s{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(2, 1, 1), Gyro(1, 1, 1)};

  IMUReading t{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(3, 1, 1), Gyro(1, 1, 1)};

  IMUReading u{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(4, 1, 1), Gyro(1, 1, 1)};

  std::size_t buffer_size(3);
  IMUBuffer imu_buffer(buffer_size);
  imu_buffer.add_readings({r, s, t, u});
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();

  std::vector<IMUReading> expected_readings{s, t, u};
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST(SensorProcessing, IMUBufferCapacityTest) {
  IMUReading r{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(1, 1, 1), Gyro(1, 1, 1)};

  IMUReading s{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(2, 1, 1), Gyro(1, 1, 1)};

  IMUReading t{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(3, 1, 1), Gyro(1, 1, 1)};

  IMUReading u{Timestamp(std::chrono::steady_clock::now().time_since_epoch()),
               Acceleration(4, 1, 1), Gyro(1, 1, 1)};

  std::size_t buffer_size(3);
  IMUBuffer imu_buffer(buffer_size);
  imu_buffer.add_readings({r, s, t, u});

  EXPECT_EQ(size(imu_buffer.get_ordered_readings()), buffer_size);
}