

#include "parser.h"

#include <iostream>
#include <string>
#include <vector>

#include "reading.h"

std::vector<Reading> parse_data_to_readings(std::vector<std::vector<std::string>>& data) {
  std::vector<Reading> readings;
  for (uint i = 1; i < data.size(); i++) {
    std::vector<std::string> row = data[i];
    if (row.size() != 5) {
      continue;
    }
    try {
      Reading r{Timestamp(row[0]), RobotID(row[1]), Velocity(row[2]), Battery(row[3]),
                Temperature(row[4])};
      readings.push_back(r);
    } catch (const std::invalid_argument& e) {
      continue;
    }
  }
  return readings;
}