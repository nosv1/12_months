#ifndef READING_H

#define READING_H
#include <string>

struct Reading {
  std::string timestamp;
  std::string robot_id;
  double velocity;
  double battery;
  double temperature;
  Reading(std::string timestamp, std::string robot_id, double velocity, double battery,
          double temperature);
  std::string to_string() const;
};

#endif