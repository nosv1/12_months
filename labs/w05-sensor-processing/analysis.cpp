#include "analysis.h"

#include <cmath>
#include <numeric>

double analysis::temperature::mean(const std::vector<TemperatureReading>& temperature_readings) {
  if (temperature_readings.empty()) {
    return std::nan("");
  }

  double sum = std::accumulate(temperature_readings.begin(), temperature_readings.end(), double{0},
                               [](double acc, const TemperatureReading& reading) {
                                 return acc + reading.temperature.degrees_c;
                               });
  return sum / size(temperature_readings);
}