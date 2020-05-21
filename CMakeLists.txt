cmake_minimum_required(VERSION 3.7.2)

project(h3)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Always make a release build
set(CMAKE_BUILD_TYPE Release)

# Build the core library as static
set(BUILD_SHARED_LIBS OFF)
set(ENABLE_BENCHMARKS OFF)
set(ENABLE_FILTERS OFF)
set(ENABLE_GENERATORS OFF)
set(ENABLE_TESTING OFF)
add_subdirectory(src/h3lib)

# Build the rest (other than the core library dependency) as shared
set(BUILD_SHARED_LIBS ON)
add_subdirectory(src/h3)
