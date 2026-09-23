#include <ctime>
#include <iostream>

#include "reading.h"

int main() {
  constexpr const char* telemetry_path = "data/sample_telemetry.csv";

  time_t now;
  // so, now is a time_t object? but time() wants a pointer to that object
  // shown by `time(time_t *__timer)` which returns a time_t??
  Reading t(time(&now), "test_id", 1, 2, 3);
  std::cout << t.to_string() << std::endl;
  return 0;
}