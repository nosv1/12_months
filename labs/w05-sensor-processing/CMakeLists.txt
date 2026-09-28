cmake_minimum_required(VERSION 3.16)

project(sensor_processing)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(sensor_processing main.cpp

target_compile_options(sensor_processing PRIVATE 
    -Wall 
    -Wextra 
    -D_GLIBCXX_ASSERTIONS 
    -fsanitize=address 
    -g)

target_link_options(sensor_processing PRIVATE
    -fsanitize=address
)