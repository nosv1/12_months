#include <fstream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::vector<std::string>> read_file(std::ifstream& file) {
  std::string line;
  std::vector<std::vector<std::string>> data;
  while (std::getline(file, line)) {
    std::vector<std::string> row;  // list of elements in line
    std::stringstream lineStream(line);
    std::string cell;
    while (std::getline(lineStream, cell, ',')) {
      row.push_back(cell);
    }
    data.push_back(row);
  }
  return data;
}