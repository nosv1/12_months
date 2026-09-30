#include "robot.h"

#include <stdexcept>
#include <string>
#include <unordered_map>

#include "sensor_buffer.h"
#include "temperature_reading.h"

Robot::Robot(const std::string& robot_id, const std::size_t temperature_buffer_size)
    : robot_id(robot_id), temperature_buffer_size(temperature_buffer_size) {};

void Robot::add_temperature_sensors(const std::vector<std::string>& buffer_names) {
  for (auto& name : buffer_names) {
    this->_temperature_sensor_buffers.emplace(
        name, SensorBuffer<TemperatureReading>{this->temperature_buffer_size});
  }
}

SensorBuffer<TemperatureReading>& Robot::get_temperature_sensor_buffer(
    const std::string& buffer_name) {
  return this->_temperature_sensor_buffers.at(buffer_name);
}
