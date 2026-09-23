#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <vector>

#include "analysis.h"
#include "grouper.h"
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

  std::map<std::string, std::vector<Reading>> robots = group_robots(parsed_lines.readings);

  for (auto& [r_id, readings] : robots) {
    std::cout << r_id << " -- " << readings.size() << " readings" << std::endl;

    std::optional<TemperatureAnalysis> opt_temperature_analysis = analyze_temperature(readings);
    if (opt_temperature_analysis != std::nullopt) {
      TemperatureAnalysis temperature_analysis =
          static_cast<TemperatureAnalysis>(*opt_temperature_analysis);
      std::cout << temperature_analysis.to_string() << std::endl;
    }
  }
  return 0;
}