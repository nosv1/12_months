
#include "analysis.h"

#include <algorithm>
#include <limits>
#include <sstream>
#include <vector>

#include "reading.h"

std::optional<TemperatureAnalysis> analyze_temperature(const std::vector<Reading>& readings) {
  TemperatureAnalysis temperature_analysis;

  if (readings.size() == 0) {
    return std::nullopt;
  }

  double min = std::numeric_limits<double>::max();
  double max = std::numeric_limits<double>::lowest();
  double sum = 0;

  for (const auto& reading : readings) {
    min = std::min(reading.temperature.v, min);
    max = std::max(reading.temperature.v, max);
    sum += reading.temperature.v;
  }
  temperature_analysis.min = min;
  temperature_analysis.max = max;
  temperature_analysis.avg = sum / readings.size();

  return temperature_analysis;
}

std::string TemperatureAnalysis::to_string() const {
  auto show = [](const std::optional<double>& v) -> std::string {
    if (!v) return "null";
    std::ostringstream oss;
    oss << *v;
    return oss.str();
  };

  std::ostringstream oss;
  oss << "min: " << show(this->min) << std::endl;
  oss << "max: " << show(this->max) << std::endl;
  oss << "avg: " << show(this->avg) << std::endl;
  return oss.str();
}