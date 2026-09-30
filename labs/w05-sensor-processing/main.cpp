#include <chrono>
#include <iostream>
#include <string>
#include <unordered_map>

#include "imu_reading.h"
#include "sensor_buffer.h"
#include "timestamp.h"

struct Robot {
  std::string robot_id;
  std::unordered_map<std::string, SensorBuffer<IMUReading>> imu_sensors;
  explicit Robot(const std::string& robot_id, const std::size_t& imu_buffer_size)
      : robot_id(robot_id) {
    for (const auto& imu_location : {"imu_front", "imu_rear", "imu_left", "imu_right"}) {
      imu_sensors.emplace(imu_location, SensorBuffer<IMUReading>(imu_buffer_size));
    }
  }
};

int main() {
  Robot robot_r{"r", std::size_t{100}};
  // std::cout << robot_r.imu_sensors << std::endl;

  return 0;
}