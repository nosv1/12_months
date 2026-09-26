cmake_minimum_required(VERSION 3.16)

project(mem)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(mem main.cpp)

target_compile_options(mem PRIVATE 
    -Wall 
    -Wextra 
    -D_GLIBCXX_ASSERTIONS 
    -fsanitize=address 
    -g)

target_link_options(mem PRIVATE
    -fsanitize=address
)