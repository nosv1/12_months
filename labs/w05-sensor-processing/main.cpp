#include <chrono>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

#include "robot.h"
#include "sensor_buffer.h"
#include "temperature_reading.h"
#include "timestamp.h"

int main() {
  // Robot robot_r{"r", std::size_t{100}};
  // for (const auto& pair : robot_r.temperature_sensor_buffers) {
  //   std::string temperature_location = pair.first;
  //   SensorBuffer<TemperatureReading> temperature_buffer = pair.second;
  //   std::cout << temperature_location << ": " << size(temperature_buffer.get_ordered_readings())
  //             << std::endl;
  // }

  // robot_r.temperature_sensor_buffers.at("battery").add_readings(
  //     {TemperatureReading{Timestamp{std::chrono::milliseconds(1)}, Temperature{1}}});

  return 0;
}