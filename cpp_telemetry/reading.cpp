#include "reading.h"

#include <iostream>
#include <sstream>
#include <string>

Reading::Reading(Timestamp timestamp, RobotID robot_id, Velocity velocity, Battery battery,
                 Temperature temperature)
    : timestamp(timestamp),
      robot_id(robot_id),
      velocity(velocity),
      battery(battery),
      temperature(temperature) {}

std::string Reading::to_string() const {
  std::ostringstream oss;
  oss << "timestamp: " << this->timestamp.v;
  oss << ", robot_id: " << this->robot_id.v;
  oss << ", velocity: " << this->velocity.v;
  oss << ", battery: " << this->battery.v;
  oss << ", temperature: " << this->temperature.v;
  return oss.str();
}