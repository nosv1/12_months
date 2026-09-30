#ifndef ROBOT_H
#define ROBOT_H

#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

#include "sensor_buffer.h"
#include "temperature_reading.h"

struct Robot {
  std::string robot_id;
  std::size_t temperature_buffer_size;
  explicit Robot(const std::string& robot_id, const std::size_t temperature_buffer_size);
  void add_temperature_sensors(const std::vector<std::string>& buffer_names);
  SensorBuffer<TemperatureReading>& get_temperature_sensor_buffer(const std::string& buffer_name);

 private:
  std::unordered_map<std::string, SensorBuffer<TemperatureReading>> _temperature_sensor_buffers;
};

#endif