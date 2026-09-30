#include <cmath>

#include <gtest/gtest.h>

#include "analysis.h"
#include "imu_reading.h"
#include "sensor_buffer.h"
#include "temperature_reading.h"
#include "timestamp.h"

class SensorProcessing : public ::testing::Test {
 protected:
  /////      IMU READINGS      /////
  std::size_t imu_buffer_size{3};
  SensorBuffer<IMUReading> imu_buffer{imu_buffer_size};
  IMUReading imu_reading_r{Timestamp(std::chrono::milliseconds(1)), Acceleration(1, 1, 1),
                           Gyro(1, 1, 1)};
  IMUReading imu_reading_s{Timestamp(std::chrono::milliseconds(2)), Acceleration(2, 1, 1),
                           Gyro(2, 1, 1)};
  IMUReading imu_reading_t{Timestamp(std::chrono::milliseconds(3)), Acceleration(3, 1, 1),
                           Gyro(3, 1, 1)};
  IMUReading imu_reading_u{Timestamp(std::chrono::milliseconds(4)), Acceleration(4, 1, 1),
                           Gyro(4, 1, 1)};
  IMUReading imu_reading_v{Timestamp(std::chrono::milliseconds(5)), Acceleration(5, 1, 1),
                           Gyro(5, 1, 1)};
  IMUReading imu_reading_w{Timestamp(std::chrono::milliseconds(6)), Acceleration(6, 1, 1),
                           Gyro(6, 1, 1)};
  IMUReading imu_reading_x{Timestamp(std::chrono::milliseconds(7)), Acceleration(7, 1, 1),
                           Gyro(7, 1, 1)};

  /////      TEMPERATURE READINGS      /////
  std::size_t temperature_buffer_size{3};
  SensorBuffer<TemperatureReading> temperature_buffer{temperature_buffer_size};
  TemperatureReading temperature_reading_r{Timestamp(std::chrono::milliseconds(1)), Temperature(1)};
  TemperatureReading temperature_reading_s{Timestamp(std::chrono::milliseconds(2)), Temperature(2)};
  TemperatureReading temperature_reading_t{Timestamp(std::chrono::milliseconds(3)), Temperature(3)};
  void add_temperature_readings() {
    temperature_buffer.add_readings(
        {temperature_reading_r, temperature_reading_s, temperature_reading_t});
  }
};

////////      SENSOR BUFFER TESTS      ////////
TEST_F(SensorProcessing, BufferSize0Test) {
  std::size_t buffer_size{0};
  EXPECT_THROW(SensorBuffer<IMUReading> buffer{buffer_size}, std::invalid_argument);
}

////////      IMU TESTS      ////////

TEST_F(SensorProcessing, IMUBufferCapacityNTest) {
  imu_buffer.add_readings({imu_reading_r, imu_reading_s, imu_reading_t});
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();
  std::vector<IMUReading> expected_readings{imu_reading_r, imu_reading_s, imu_reading_t};
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST_F(SensorProcessing, IMUBufferEmptyTest) {
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();
  std::vector<IMUReading> expected_readings;
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST_F(SensorProcessing, IMUBufferNotFullTest) {
  imu_buffer.add_readings({imu_reading_r, imu_reading_s});
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();
  std::vector<IMUReading> expected_readings{imu_reading_r, imu_reading_s};
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST_F(SensorProcessing, IMUBufferOrderTest) {
  imu_buffer.add_readings({imu_reading_r, imu_reading_s, imu_reading_t, imu_reading_u,
                           imu_reading_v, imu_reading_w, imu_reading_x});
  std::vector<IMUReading> ordered_imu_readings = imu_buffer.get_ordered_readings();
  std::vector<IMUReading> expected_readings{imu_reading_v, imu_reading_w, imu_reading_x};
  EXPECT_EQ(ordered_imu_readings, expected_readings);
}

TEST_F(SensorProcessing, IMUBufferCapacityTest) {
  std::size_t buffer_size = 3;
  SensorBuffer<IMUReading> imu_buffer{buffer_size};
  imu_buffer.add_readings({imu_reading_r, imu_reading_s, imu_reading_t, imu_reading_u});
  EXPECT_EQ(size(imu_buffer.get_ordered_readings()), buffer_size);
}

////////      TEMPERATURE TESTS      ////////
TEST_F(SensorProcessing, TemperatureBufferOrderTest) {
  std::size_t buffer_size{2};
  SensorBuffer<TemperatureReading> temperature_buffer(buffer_size);
  temperature_buffer.add_readings(
      {temperature_reading_r, temperature_reading_s, temperature_reading_t});
  std::vector<TemperatureReading> ordered_temperature_readings =
      temperature_buffer.get_ordered_readings();
  std::vector<TemperatureReading> expected_readings{temperature_reading_s, temperature_reading_t};
  EXPECT_EQ(ordered_temperature_readings, expected_readings);
}

TEST_F(SensorProcessing, TemperatureMeanWith0ReadingsTest) {
  std::size_t buffer_size{3};
  SensorBuffer<TemperatureReading> temperature_buffer_(buffer_size);
  EXPECT_TRUE(std::isnan(analysis::temperature::mean(temperature_buffer_.get_ordered_readings())));
}

TEST_F(SensorProcessing, TemperatureMeanTest) {
  std::size_t buffer_size{3};
  SensorBuffer<TemperatureReading> temperature_buffer_(buffer_size);
  temperature_buffer_.add_readings(
      {temperature_reading_r, temperature_reading_s, temperature_reading_t});
  EXPECT_DOUBLE_EQ(analysis::temperature::mean(temperature_buffer_.get_ordered_readings()), 2);
}