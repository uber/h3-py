cmake_minimum_required(VERSION 3.15...3.26)

project(${SKBUILD_PROJECT_NAME} LANGUAGES C)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Always make a release build
set(CMAKE_BUILD_TYPE Release)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED)

# Avoid building tooling we won't need for release
# See all options with `cmake -LA` in an `h3/build` directory,
# or at https://h3geo.org/docs/next/core-library/compilation-options/
macro(turn_off option_name)
    set(${option_name} OFF CACHE BOOL "" FORCE)
endmacro()
turn_off(BUILD_ALLOC_TESTS)
turn_off(BUILD_BENCHMARKS)
turn_off(BUILD_FILTERS)
turn_off(BUILD_FUZZERS)
turn_off(BUILD_GENERATORS)
turn_off(BUILD_TESTING)
turn_off(ENABLE_COVERAGE)
turn_off(ENABLE_DOCS)
turn_off(ENABLE_FORMAT)
turn_off(ENABLE_LIBFUZZER)
turn_off(ENABLE_LINTING)

# Build the core library as static
set(BUILD_SHARED_LIBS OFF)
add_subdirectory(src/h3lib)

# Build the rest (other than the core library dependency) as shared
set(BUILD_SHARED_LIBS ON)
add_subdirectory(src/h3)

# Include built h3api.h for Cython API
install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/src/h3lib/src/h3lib/include/h3api.h"
    DESTINATION
        ${SKBUILD_PROJECT_NAME}/_cy)
