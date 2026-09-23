cmake_minimum_required(VERSION 3.16)

project(telem)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(telem main.cpp reading.cpp)

target_compile_options(telem PRIVATE -Wall -Wextra -D_GLIBCXX_ASSERTIONS)