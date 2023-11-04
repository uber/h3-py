find_package(Cython MODULE REQUIRED)
find_package(PythonExtensions MODULE REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Build Cython annotations
set(CYTHON_ANNOTATE TRUE)

macro(add_cython_file filename)
    add_cython_target(${filename} C PY3)
    add_library(${filename} MODULE ${filename} ${LIB_SOURCE_FILES} ${CONFIGURED_API_HEADER})
    python_extension_module(${filename})
    set_property(TARGET ${filename} PROPERTY C_STANDARD 99)
    target_link_libraries(${filename} h3)
    install(TARGETS ${filename} LIBRARY DESTINATION src/h3/_cy)
endmacro()

# GLOB pattern is recommended against
# https://cmake.org/cmake/help/v3.14/command/file.html?highlight=file#filesystem
add_cython_file(util)
add_cython_file(latlng)
add_cython_file(cells)
add_cython_file(edges)
add_cython_file(to_multipoly)
add_cython_file(error_system)
add_cython_file(memory)


# Include pyx and pxd files in distribution for use by Cython API
install(
    FILES
        cells.pxd
        cells.pyx
        edges.pxd
        edges.pyx
        latlng.pxd
        latlng.pyx
        h3lib.pxd
        util.pxd
        util.pyx
        error_system.pyx
        memory.pxd
        memory.pyx
    DESTINATION
        src/h3/_cy
)
