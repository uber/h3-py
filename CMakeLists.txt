cmake_minimum_required(VERSION 3.3)

set(version_regex "^version = '([0-9.]+)'$")
file(STRINGS "version.py" version_line
     REGEX "${version_regex}")
string(REGEX MATCH "${version_regex}" _ "${version_line}")
set(version "${CMAKE_MATCH_1}")
message(STATUS "h3core-py version: ${version}")

set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_SOURCE_DIR}/cmake/toolchain.cmake"
    CACHE STRING "Toolchain file to build project and dependencies")

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
include(HunterGate)

HunterGate(URL "https://github.com/ruslo/hunter/archive/v0.22.17.tar.gz"
           SHA1 "b89a5110e8e417dcac552f66b640bb3735e0b898")

project(h3core-py VERSION "${version}" LANGUAGES C CXX)

find_package(Cython REQUIRED)
find_package(PythonExtensions REQUIRED)
find_package(PythonLibs REQUIRED)

hunter_add_package(h3)
find_package(h3 CONFIG REQUIRED)

add_cython_target(h3core_cy h3core.pyx)
add_library(h3core MODULE ${h3core_cy})
python_extension_module(h3core)
target_link_libraries(h3core h3::h3)
