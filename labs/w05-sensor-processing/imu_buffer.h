#ifndef IMU_BUFFER_H

#define IMU_BUFFER_H

#include <string>
#include <vector>

#include "imu_reading.h"

class IMUBuffer {
  std::size_t _buffer_size;
  std::vector<IMUReading> _imu_readings;
  uint _tail_idx = 0;
  void _add_reading(const IMUReading& imu_reading);
  void _set_buffer_size(const std::size_t& buffer_size);
  uint _insert_idx();

 public:
  explicit IMUBuffer(const std::size_t& buffer_size);
  void add_readings(const std::vector<IMUReading>& imu_readings);
  std::vector<IMUReading> get_readings();
  std::string to_string();
};

#endif