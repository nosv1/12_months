#ifndef PARSER_H

#define PARSER_H

#include <string>
#include <vector>

#include "reading.h"

struct ParsedLines {
  std::vector<Reading> readings;
  std::vector<std::vector<std::string>> bad_rows;
};

ParsedLines parse_data(std::vector<std::vector<std::string>>& data);

#endif