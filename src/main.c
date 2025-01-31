#include <stdint.h>
#include <stdio.h>
#include "pico/stdlib.h"

extern void    setLogFunction(void (*log_function)(uint8_t *string));
extern int16_t predict(void *input, void *output);


static void log_fn(uint8_t *string) {
    printf("%s\n", string);
}


int main() {
    setLogFunction(log_fn);

    setup_default_uart();

    double input[3] = {1.23, 4.56, 6.78};

    printf("Hello, world %i!\n", predict(input, NULL));
    return 0;
}
