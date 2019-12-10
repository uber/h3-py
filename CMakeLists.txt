cmake_minimum_required(VERSION 3.7.2)

project(h3)

# Build the core library as static
set(BUILD_SHARED_LIBS OFF)
add_subdirectory(src/h3lib)

# Build the rest (other than the core library dependency) as shared
set(BUILD_SHARED_LIBS ON)
add_subdirectory(src/h3)
