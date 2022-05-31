cmake_minimum_required(VERSION 3.7.2)

project(h3)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Always make a release build
set(CMAKE_BUILD_TYPE Release)

# Avoid building tooling we won't need for release
set(BUILD_BENCHMARKS OFF CACHE BOOL "" FORCE)
set(BUILD_FILTERS OFF CACHE BOOL "" FORCE)
set(BUILD_GENERATORS OFF CACHE BOOL "" FORCE)
set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
set(ENABLE_DOCS OFF CACHE BOOL "" FORCE)

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
        src/h3/_cy)
