cmake_minimum_required(VERSION 3.16)

project(sensor_processing)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_library(sensor_processing_library
  imu_reading.cpp
  temperature_reading.cpp
  timestamp.cpp
)
add_executable(sensor_processing main.cpp)
target_link_libraries(sensor_processing PRIVATE sensor_processing_library)
target_compile_options(sensor_processing_library PRIVATE 
    -Wall 
    -Wextra 
    -D_GLIBCXX_ASSERTIONS 
    -fsanitize=address 
    -g
  )
target_link_options(sensor_processing_library INTERFACE
    -fsanitize=address
)

# testing
enable_testing()

add_executable(
  sensor_processing_test
  sensor_processing_test.cpp
)
target_link_libraries(
  sensor_processing_test
  GTest::gtest_main
  sensor_processing_library
)

include(GoogleTest)
gtest_discover_tests(sensor_processing_test)