cmake_minimum_required(VERSION 3.7.2)

set(version_regex "([0-9.]+)")
file(STRINGS "src/h3lib/VERSION" h3_version
     REGEX "^${version_regex}$")
message(STATUS "h3 version: ${h3_version}")

set(py_version_regex "^version = '${version_regex}'$")
file(STRINGS "src/h3/_version.py" version_line
     REGEX "${py_version_regex}")
string(REGEX MATCH "${py_version_regex}" _ "${version_line}")
set(version "${CMAKE_MATCH_1}")
message(STATUS "h3core-py version: ${version}")

project(h3 VERSION "${version}")

# Build the core library as static
set(BUILD_SHARED_LIBS OFF)
add_subdirectory(src/h3lib)

# Build the rest (other than the core library dependency) as shared
set(BUILD_SHARED_LIBS ON)
add_subdirectory(src/h3)
