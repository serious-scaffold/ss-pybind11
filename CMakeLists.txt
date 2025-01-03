cmake_minimum_required(VERSION 3.25)
message(STATUS "CMAKE VERSION:${CMAKE_VERSION}")

project(
  ss_pybind11
  LANGUAGES CXX C
  HOMEPAGE_URL "https://github.com/serious-scaffold/ss-pybind11"
  DESCRIPTION "A template of serious scaffold family based on pybind11.")

# Project default module
find_package(cmake-modules REQUIRED)
include(cmake-modules/ProjectDefault)

# Project custom modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(ConfigureVersion)

add_subdirectory(src)
