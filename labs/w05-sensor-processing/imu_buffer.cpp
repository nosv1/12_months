#include "imu_buffer.h"

#include <iostream>
#include <sstream>
#include <string>

#include "imu_reading.h"

void IMUBuffer::_set_buffer_size(const std::size_t& buffer_size) {
  this->_buffer_size = buffer_size;
}

IMUBuffer::IMUBuffer(const std::size_t& buffer_size) {
  this->_set_buffer_size(buffer_size);
  this->_imu_readings.reserve(this->_buffer_size);
}

uint IMUBuffer::_insert_idx() { return (this->_tail_idx + 1) % this->_buffer_size; }

void IMUBuffer::_add_reading(const IMUReading& imu_reading) {
  if (size(this->_imu_readings) < this->_buffer_size) {
    this->_tail_idx = size(this->_imu_readings);
    this->_imu_readings.push_back(imu_reading);

  } else {
    uint insert_idx = this->_insert_idx();
    this->_imu_readings[insert_idx] = imu_reading;
    this->_tail_idx = insert_idx;
  }
}

void IMUBuffer::add_readings(const std::vector<IMUReading>& imu_readings) {
  for (auto const& imu_reading : imu_readings) {
    this->_add_reading(imu_reading);
  }
}

std::vector<IMUReading> IMUBuffer::get_readings() { return this->_imu_readings; }

std::string IMUBuffer::to_string() {
  std::ostringstream oss;
  oss << "size: " << size(this->_imu_readings) << " of " << this->_buffer_size;
  return oss.str();
}