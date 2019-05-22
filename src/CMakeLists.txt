find_package(Cython MODULE REQUIRED)
find_package(PythonExtensions MODULE REQUIRED)
# find_package(PythonLibs MODULE REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
# add_cython_target(h3core_cy "${CMAKE_CURRENT_SOURCE_DIR}/h3core.pyx")
add_cython_target(h3core C PY3)
# add_library(h3core MODULE ${h3core_cy})
add_library(h3core MODULE ${h3core} ${LIB_SOURCE_FILES} ${CONFIGURED_API_HEADER})
python_extension_module(h3core)
set_property(TARGET h3core PROPERTY C_STANDARD 99)

target_compile_definitions(h3core INTERFACE $<TARGET_PROPERTY:h3,COMPILE_DEFINITIONS>)
target_include_directories(h3core INTERFACE $<TARGET_PROPERTY:h3,INCLUDE_DIRECTORIES>)
target_link_libraries(h3core h3)

# target_include_directories(_h3 PUBLIC
# $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/h3lib/include>
# $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/h3lib/include>)

install(TARGETS h3core LIBRARY DESTINATION src)
