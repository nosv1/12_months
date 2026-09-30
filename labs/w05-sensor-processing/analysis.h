#ifndef ANALYSIS_H
#define ANALYSIS_H

#include <vector>

#include "temperature_reading.h"

namespace analysis {
namespace temperature {
double mean(const std::vector<TemperatureReading>& temperature_readings);
}  // namespace temperature
}  // namespace analysis
#endif