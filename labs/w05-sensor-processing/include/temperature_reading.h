#ifndef TEMPERATURE_READING_H

#define TEMPERATURE_READING_H

#include <string>

#include "timestamp.h"

// TEMPERATURE READING

struct Temperature {
  double degrees_c;
  explicit Temperature(double degrees_c) : degrees_c(degrees_c) {}
  bool operator==(const Temperature& other) const;
  std::string to_string() const;
};

struct TemperatureReading {
  Timestamp timestamp;
  Temperature temperature;
  explicit TemperatureReading(Timestamp timestamp, Temperature temperature)
      : timestamp(timestamp), temperature(temperature) {}
  bool operator==(const TemperatureReading& other) const;
  std::string to_string() const;
};

std::ostream& operator<<(std::ostream& os, const TemperatureReading& r);

#endif