cmake_minimum_required(VERSION 3.7.2)

project(h3)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(MINGW)
    message(STATUS "MinGW:")
    if(BIT MATCHES "64")
        add_definitions(-DMS_WIN64)
    endif(BIT MATCHES "64")
endif(MINGW)

# Build the core library as static
set(BUILD_SHARED_LIBS OFF)
add_subdirectory(src/h3lib)

# Build the rest (other than the core library dependency) as shared
set(BUILD_SHARED_LIBS ON)
add_subdirectory(src/h3)
