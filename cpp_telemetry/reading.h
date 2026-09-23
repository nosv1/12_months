#ifndef READING_H

#define READING_H

#include <string>

struct Reading {
  time_t timestamp;
  std::string robot_id;
  double velocity;
  double battery;
  double temperature;
  Reading(time_t timestamp, std::string robot_id, double velocity, double battery,
          double temperature);
  std::string to_string() const;
};

#endif