cmake_minimum_required(VERSION 3.4...3.18)
project(Excel2CSV)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)
find_package(xlnt REQUIRED)

pybind11_add_module(Excel2CSV bindings/bindings.cpp)

target_link_libraries(Excel2CSV PRIVATE xlnt::xlnt)
