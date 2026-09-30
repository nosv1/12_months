#include <gtest/gtest.h>

#include "imu_reading.h"
#include "sensor_buffer.h"
#include "timestamp.h"

class SensorProcessing : public ::testing::Test {
 protected:
  std::size_t buffer_size{3};
  SensorBuffer<IMUReading> imu_buffer{buffer_size};
  IMUReading r_imu_reading{Timestamp(std::chrono::milliseconds(1)), Acceleration(1, 1, 1),
                           Gyro(1, 1, 1)};
  IMUReading s_imu_reading{Timestamp(std::chrono::milliseconds(2)), Acceleration(2, 1, 1),
                           Gyro(2, 1, 1)};
  IMUReading t_imu_reading{Timestamp(std::chrono::milliseconds(3)), Acceleration(3, 1, 1),
                           Gyro(3, 1, 1)};
  IMUReading u_imu_reading{Timestamp(std::chrono::milliseconds(4)), Acceleration(4, 1, 1),
                           Gyro(4, 1, 1)};
  IMUReading v_imu_reading{Timestamp(std::chrono::milliseconds(5)), Acceleration(5, 1, 1),
                           Gyro(5, 1, 1)};
  IMUReading w_imu_reading{Timestamp(std::chrono::milliseconds(6)), Acceleration(6, 1, 1),
                           Gyro(6, 1, 1)};
  IMUReading x_imu_reading{Timestamp(std::chrono::milliseconds(7)), Acceleration(7, 1, 1),
                           Gyro(7, 1, 1)};
};

TEST_F(SensorProcessing, IMUBufferCapacityNTest) {
  imu_buffer.add_readings({r_imu_reading, s_imu_reading, t_imu_reading});
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();
  std::vector<IMUReading> expected_readings{r_imu_reading, s_imu_reading, t_imu_reading};
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST_F(SensorProcessing, IMUBufferEmptyTest) {
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();
  std::vector<IMUReading> expected_readings;
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST_F(SensorProcessing, IMUBufferNotFullTest) {
  imu_buffer.add_readings({r_imu_reading, s_imu_reading});
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();
  std::vector<IMUReading> expected_readings{r_imu_reading, s_imu_reading};
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST_F(SensorProcessing, IMUBufferOrderTest) {
  imu_buffer.add_readings({r_imu_reading, s_imu_reading, t_imu_reading, u_imu_reading,
                           v_imu_reading, w_imu_reading, x_imu_reading});
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();
  std::vector<IMUReading> expected_readings{v_imu_reading, w_imu_reading, x_imu_reading};
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST_F(SensorProcessing, IMUBufferCapacityTest) {
  imu_buffer.add_readings({r_imu_reading, s_imu_reading, t_imu_reading, u_imu_reading});
  EXPECT_EQ(size(imu_buffer.get_ordered_readings()), buffer_size);
}