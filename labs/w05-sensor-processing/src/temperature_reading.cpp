

#include "temperature_reading.h"

#include <sstream>
#include <string>

// TEMPERATURE

bool Temperature::operator==(const Temperature& other) const {
  return this->degrees_c == other.degrees_c;
}

std::string Temperature::to_string() const {
  std::ostringstream oss;
  oss << "temperature (C): " << this->degrees_c;
  return oss.str();
}

// TEMPERATURE READING

bool TemperatureReading::operator==(const TemperatureReading& other) const {
  return this->timestamp == other.timestamp && this->temperature == other.temperature;
}

std::string TemperatureReading::to_string() const {
  std::ostringstream oss;
  oss << "timestamp: " << this->timestamp.to_string() << std::endl;
  oss << this->temperature.to_string() << std::endl;
  return oss.str();
}

std::ostream& operator<<(std::ostream& os, const TemperatureReading& r) {
  return os << r.to_string();
};