#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "parser.h"
#include "reader.h"
#include "reading.h"

int main() {
  constexpr const char* telemetry_path = "data/sample_telemetry.csv";

  std::ifstream file(telemetry_path);  // opens the file
  if (!file.is_open()) {
    std::cerr << "Could not open the file." << std::endl;
    return 1;
  }
  std::vector<std::vector<std::string>> data = read_file(file);
  file.close();

  ParsedLines parsed_lines = parse_data_to_readings(data);
  std::cout << "Readings: " << parsed_lines.readings.size() << std::endl;
  std::cout << "Rejected readings: " << parsed_lines.bad_rows.size() << std::endl;
  return 0;
}