#include <iostream>

#include "reading.h"

int main() {
  constexpr const char* telemetry_path = "data/sample_telemetry.csv";

  Reading t("2026-09-03T14:00:02.027Z", "test_id", 1, 2, 3);
  std::cout << t.to_string() << std::endl;
  return 0;
}