#ifndef ANALYSIS_H

#define ANALYSIS_H

#include <optional>
#include <vector>

#include "reading.h"

struct TemperatureAnalysis {
  double min;
  double max;
  double avg;
  std::string to_string() const;
};

std::optional<TemperatureAnalysis> analyze_temperature(const std::vector<Reading>& readings);

#endif