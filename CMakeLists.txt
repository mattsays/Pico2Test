cmake_minimum_required(VERSION 3.13...3.27)

set(libneural_network_a "${CMAKE_SOURCE_DIR}/lib/neural_network/zig-out/lib/libneural_network.a")

add_custom_command(
  OUTPUT "${libneural_network_a}"
  COMMAND cd ${CMAKE_SOURCE_DIR}/lib/neural_network && zig build lib -Dtarget=thumb-freestanding -Dcpu=cortex_m33
  )
add_custom_target(libneural_network DEPENDS "${libneural_network_a}")

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(pi_pico_zant CXX C ASM)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

# rest of your project
add_executable(main
    src/main.c
)
add_dependencies(main libneural_network)
target_link_libraries(main "${libneural_network_a}")

# Add pico_stdlib library which aggregates commonly used features
target_link_libraries(main pico_stdlib)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(main)
