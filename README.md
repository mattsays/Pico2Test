# Building

You need to install the [Pi Pico SDK](https://github.com/raspberrypi/pico-sdk.git); follow [this guide](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf) to do so.
Prepare your environment by filling `PICO_SDK_PATH` with your install location; example:

```sh
$ export PICO_SDK_PATH=~/Source/pico-sdk/
```

Then, build the project with cmake (the following commands target the Pi Pico 2):

```sh
$ mkdir build
$ cd build
$ cmake .. -DPICO_PLATFORM=rp2350 -DPICO_BOARD=pico2
$ make
```

This will eventually create a few interesting outputs:

 - `main.uf2`: this can be loaded directly via USB. Just attach the Pi Pico to your machine while holding down the BOOT button on the board; it should present itself as thumb drive. Copy `main.uf2` in the drive to load the firmware.
 - `main.elf`: ELF files can be loaded with a debugger. Make sure you have a session of openocd running (for example, `openocd -f interface/cmsis-dap.cfg -f target/rp2350.cfg -c "adapter speed 5000"` for the Pi Pico 2); then run `arm-none-eabi-gdb main.elf -ex "target extended-remote localhost:3333" -ex "monitor arm semihosting enable" -ex "monitor reset init" -ex "load"` to load `main.elf` on the board and start a command line debugging session.
