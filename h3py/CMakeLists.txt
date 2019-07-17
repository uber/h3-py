find_package(Cython MODULE REQUIRED)
find_package(PythonExtensions MODULE REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
add_cython_target(h3core C PY3)
add_library(h3core MODULE ${h3core} ${LIB_SOURCE_FILES} ${CONFIGURED_API_HEADER})
python_extension_module(h3core)
set_property(TARGET h3core PROPERTY C_STANDARD 99)
target_compile_definitions(h3core INTERFACE $<TARGET_PROPERTY:h3,COMPILE_DEFINITIONS>)
target_include_directories(h3core INTERFACE $<TARGET_PROPERTY:h3,INCLUDE_DIRECTORIES>)
target_link_libraries(h3core h3)

add_cython_target(util C PY3)
add_library(util MODULE ${util} ${LIB_SOURCE_FILES} ${CONFIGURED_API_HEADER})
python_extension_module(util)
set_property(TARGET util PROPERTY C_STANDARD 99)
target_compile_definitions(util PUBLIC $<TARGET_PROPERTY:h3,COMPILE_DEFINITIONS>)
target_include_directories(util PUBLIC $<TARGET_PROPERTY:h3,INCLUDE_DIRECTORIES>)

install(TARGETS h3core util LIBRARY DESTINATION h3py)


add_cython_target(geo C PY3)
add_library(geo MODULE ${geo} ${LIB_SOURCE_FILES} ${CONFIGURED_API_HEADER})
python_extension_module(geo)
set_property(TARGET geo PROPERTY C_STANDARD 99)
target_compile_definitions(geo PUBLIC $<TARGET_PROPERTY:h3,COMPILE_DEFINITIONS>)
target_include_directories(geo PUBLIC $<TARGET_PROPERTY:h3,INCLUDE_DIRECTORIES>)

install(TARGETS h3core geo LIBRARY DESTINATION h3py)
