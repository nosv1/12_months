#include <map>
#include <string>
#include <vector>

#include "reading.h"

std::map<std::string, std::vector<Reading>> group_robots(const std::vector<Reading>& readings) {
  std::map<std::string, std::vector<Reading>> robots;
  for (const auto& reading : readings) {
    // not needed map[key] inserts, if not present, dangerous if just checking tho
    // if (robots.find(reading.robot_id.v) == robots.end()) {
    //   robots[reading.robot_id.v] = {};
    // }
    robots[reading.robot_id.v].push_back(reading);
  }
  return robots;
}