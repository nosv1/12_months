#ifndef READING_H

#define READING_H
#include <string>

struct Timestamp {
  std::string v;
  Timestamp(std::string v) { this->v = v; }
};

struct RobotID {
  std::string v;
  RobotID(std::string v) { this->v = v; }
};

struct Velocity {
  double v;
  Velocity(std::string v) { this->v = std::stod(v); }
};

struct Battery {
  double v;
  Battery(std::string v) { this->v = std::stod(v); }
};
struct Temperature {
  double v;
  Temperature(std::string v) { this->v = std::stod(v); }
};

struct Reading {
  Timestamp timestamp;
  RobotID robot_id;
  Velocity velocity;
  Battery battery;
  Temperature temperature;
  Reading(Timestamp timestamp, RobotID robot_id, Velocity velocity, Battery battery,
          Temperature temperature);
  std::string to_string() const;
};

#endif