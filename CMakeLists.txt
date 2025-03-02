cmake_minimum_required(VERSION 3.13...3.27)

set(PICO_PLATFORM "rp2350")
set(PICO_BOARD "pico2")

set(libneural_network_a "${CMAKE_SOURCE_DIR}/lib/libstatic_lib.a")

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

target_link_libraries(main "${libneural_network_a}")

# Add pico_stdlib library which aggregates commonly used features
target_link_libraries(main pico_stdlib)

# Enable USB output, disable uart output
pico_enable_stdio_usb(main 1)
pico_enable_stdio_uart(main 0)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(main)
