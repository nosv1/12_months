#ifndef READING_H

#define READING_H
#include <string>

struct Timestamp {
  std::string v;
  explicit Timestamp(std::string v) { this->v = v; }
};

struct RobotID {
  std::string v;
  explicit RobotID(std::string v) { this->v = v; }
};

struct Velocity {
  double v;
  explicit Velocity(std::string v) { this->v = std::stod(v); }
};

struct Battery {
  double v;
  explicit Battery(std::string v) { this->v = std::stod(v); }
};
struct Temperature {
  double v;
  explicit Temperature(std::string v) { this->v = std::stod(v); }
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