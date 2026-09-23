#include "reading.h"

#include <sstream>
#include <string>

Reading::Reading(std::string timestamp, std::string robot_id, double velocity, double battery,
                 double temperature)
    : timestamp(timestamp),
      robot_id(robot_id),
      velocity(velocity),
      battery(battery),
      temperature(temperature) {}

std::string Reading::to_string() const {
  std::ostringstream oss;
  oss << "timestamp: " << this->timestamp;
  oss << ", robot_id: " << this->robot_id;
  oss << ", velocity: " << this->velocity;
  oss << ", battery: " << this->battery;
  oss << ", temperature: " << this->temperature;
  return oss.str();
}