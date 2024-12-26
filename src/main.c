#include <stdint.h>
#include <stdio.h>
#include "pico/stdlib.h"


extern int16_t infer(void);


int main() {
    setup_default_uart();

    printf("Hello, world %i!\n", infer());
    return 0;
}
