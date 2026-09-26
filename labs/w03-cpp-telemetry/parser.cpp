

#include "parser.h"

#include <iostream>
#include <string>
#include <vector>

#include "reading.h"

ParsedLines parse_data(const std::vector<std::vector<std::string>>& data) {
  ParsedLines parsed_lines;

  for (uint i = 1; i < data.size(); i++) {
    std::vector<std::string> row = data[i];
    if (row.size() != 5) {
      parsed_lines.bad_rows.push_back(row);
      continue;
    }
    try {
      Reading r{Timestamp(row[0]), RobotID(row[1]), Velocity(row[2]), Battery(row[3]),
                Temperature(row[4])};
      parsed_lines.readings.push_back(r);
    } catch (const std::invalid_argument& e) {
      parsed_lines.bad_rows.push_back(row);
      continue;
    }
  }
  return parsed_lines;
}