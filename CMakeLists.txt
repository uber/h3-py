cmake_minimum_required(VERSION 3.11.0)

set(BUILD_SHARED_LIBS ON)

set(version_regex "([0-9.]+)")
file(STRINGS "h3/VERSION" h3_version
     REGEX "^${version_regex}$")
message(STATUS "h3 version: ${h3_version}")

set(py_version_regex "^version = '${version_regex}'$")
file(STRINGS "version.py" version_line
     REGEX "${py_version_regex}")
string(REGEX MATCH "${py_version_regex}" _ "${version_line}")
set(version "${CMAKE_MATCH_1}")
message(STATUS "h3core-py version: ${version}")

project(h3core-py VERSION "${version}" LANGUAGES C CXX)

add_subdirectory(h3)

find_package(Cython MODULE REQUIRED)
find_package(PythonExtensions MODULE REQUIRED)
find_package(PythonLibs MODULE REQUIRED)

add_cython_target(h3core_cy "${CMAKE_CURRENT_SOURCE_DIR}/h3core.pyx")
add_library(h3core MODULE ${h3core_cy})
python_extension_module(h3core)

target_compile_definitions(h3core INTERFACE $<TARGET_PROPERTY:h3,COMPILE_DEFINITIONS>)
target_include_directories(h3core INTERFACE $<TARGET_PROPERTY:h3,INCLUDE_DIRECTORIES>)
target_link_libraries(h3core h3)

install(TARGETS h3core LIBRARY DESTINATION h3core)
