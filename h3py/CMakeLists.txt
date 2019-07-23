find_package(Cython MODULE REQUIRED)
find_package(PythonExtensions MODULE REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

macro(add_cython_file filename)
    add_cython_target(${filename} C PY3)
    add_library(${filename} MODULE ${filename} ${LIB_SOURCE_FILES} ${CONFIGURED_API_HEADER})
    python_extension_module(${filename})
    set_property(TARGET ${filename} PROPERTY C_STANDARD 99)
    target_compile_definitions(${filename} PUBLIC $<TARGET_PROPERTY:h3,COMPILE_DEFINITIONS>)
    target_include_directories(${filename} PUBLIC $<TARGET_PROPERTY:h3,INCLUDE_DIRECTORIES>)
    install(TARGETS h3core ${filename} LIBRARY DESTINATION h3py)
endmacro()

add_cython_file(h3core)
add_cython_file(util)
add_cython_file(geo)

target_link_libraries(h3core h3)
