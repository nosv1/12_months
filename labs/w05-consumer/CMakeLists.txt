cmake_minimum_required(VERSION 3.21)

project(consumer)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory("../w05-sensor-processing" "sensor_processing_library" EXCLUDE_FROM_ALL)

add_executable(consumer main.cpp)
target_link_libraries(consumer PRIVATE sensor_processing_library)