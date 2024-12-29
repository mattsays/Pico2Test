cmake_minimum_required(VERSION 3.13...3.27)

include(FetchContent)

function(CloneRepository repositoryURL branchName projectName sourceDir)
  #Commands are left empty so that we only checkout the source and no not perform any kind of build
  message("Starting to clone ${projectName} into ${sourceDir}")
  FetchContent_Declare(
    "${projectName}"
    GIT_REPOSITORY "${repositoryURL}"
    SOURCE_DIR "${sourceDir}"
    GIT_TAG "origin/${branchName}"
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
  )
  FetchContent_MakeAvailable(${projectName})
endfunction(CloneRepository)

#set(libZant_a "${CMAKE_BINARY_DIR}/Z-ant/zig-out/lib/libZant.a")
set(libZant_a "${CMAKE_BINARY_DIR}/libZant.a")

CloneRepository("https://github.com/ZIGTinyBook/Z-Ant" "embedded" Zant "${CMAKE_BINARY_DIR}/Z-ant")
add_custom_command(
  OUTPUT "${libZant_a}"
  COMMAND cd ${CMAKE_BINARY_DIR}/Z-ant && zig build lib -Dmodel=exportTryModel.bin -Dtarget=thumb-freestanding -Dcpu=cortex_m0
  )
add_custom_target(libZant DEPENDS "${libZant_a}")

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
add_dependencies(main libZant)
target_link_libraries(main "${libZant_a}")

# Add pico_stdlib library which aggregates commonly used features
target_link_libraries(main pico_stdlib)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(main)
