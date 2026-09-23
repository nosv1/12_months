#ifndef PARSER_H

#define PARSER_H

#include <string>
#include <vector>

#include "reading.h"

std::vector<Reading> parse_data_to_readings(std::vector<std::vector<std::string>>& data);

#endif