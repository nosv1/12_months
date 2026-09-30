#ifndef SENSOR_BUFFER_H

#define SENSOR_BUFFER_H

#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

template <typename T>
class SensorBuffer {
  std::size_t _buffer_size;
  std::vector<T> _readings;
  uint _tail_idx = 0;
  void _add_reading(const T& reading);
  void _set_buffer_size(const std::size_t& buffer_size);
  uint _insert_idx();

 public:
  explicit SensorBuffer(const std::size_t& buffer_size);
  void add_readings(const std::vector<T>& readings);
  std::vector<T> get_ordered_readings() const;
  std::string to_string() const;
};

template <typename T>
void SensorBuffer<T>::_set_buffer_size(const std::size_t& buffer_size) {
  if (buffer_size == 0) {
    throw std::invalid_argument("Buffer size must be > 0");
  }
  this->_buffer_size = buffer_size;
}

template <typename T>
SensorBuffer<T>::SensorBuffer(const std::size_t& buffer_size) {
  this->_set_buffer_size(buffer_size);
  this->_readings.reserve(this->_buffer_size);
}

template <typename T>
uint SensorBuffer<T>::_insert_idx() {
  return (this->_tail_idx + 1) % this->_buffer_size;
}

template <typename T>
void SensorBuffer<T>::_add_reading(const T& reading) {
  if (size(this->_readings) < this->_buffer_size) {
    this->_tail_idx = size(this->_readings);
    this->_readings.push_back(reading);

  } else {
    uint insert_idx = this->_insert_idx();
    this->_readings[insert_idx] = reading;
    this->_tail_idx = insert_idx;
  }
}

template <typename T>
void SensorBuffer<T>::add_readings(const std::vector<T>& readings) {
  for (auto const& reading : readings) {
    this->_add_reading(reading);
  }
}

template <typename T>
std::vector<T> SensorBuffer<T>::get_ordered_readings() const {
  std::vector<T> ordered_readings;
  ordered_readings.reserve(size(this->_readings));

  uint i = this->_tail_idx;
  while (size(ordered_readings) < size(this->_readings)) {
    i = (i + 1) % size(this->_readings);
    ordered_readings.push_back(this->_readings[i]);
  }

  return ordered_readings;
}

template <typename T>
std::string SensorBuffer<T>::to_string() const {
  std::ostringstream oss;
  oss << "size: " << size(this->_readings) << " of " << this->_buffer_size;
  return oss.str();
}

#endif