#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "reading.h"

std::vector<std::vector<std::string>> read_file(std::ifstream& file) {
  std::string line;
  std::vector<std::vector<std::string>> data;
  while (std::getline(file, line)) {
    std::vector<std::string> row;  // list of elements in line
    std::stringstream lineStream(line);
    std::string cell;
    while (std::getline(lineStream, cell, ',')) {
      row.push_back(cell);
    }
    data.push_back(row);
  }
  return data;
}

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

int main() {
  constexpr const char* telemetry_path = "data/sample_telemetry.csv";

  std::ifstream file(telemetry_path);  // opens the file
  if (!file.is_open()) {
    std::cerr << "Could not open the file." << std::endl;
    return 1;
  }
  std::vector<std::vector<std::string>> data = read_file(file);
  file.close();

  std::vector<Reading> readings = parse_data_to_readings(data);
  std::cout << "Readings: " << readings.size() << std::endl;
  std::cout << "Rejected readings: " << data.size() - (readings.size() - 1) << std::endl;
  return 0;
}