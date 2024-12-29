#include <stdint.h>
#include <stdio.h>
#include "pico/stdlib.h"

extern void    set_log_function(void (*log_function)(uint8_t *string));
extern void    set_timestamp_function(uint64_t (*timestamp_function)(void));
extern int16_t infer();


static void log_fn(uint8_t *string) {
    printf("%s\n", string);
}


static uint64_t timestamp_fn(void) {
    return to_us_since_boot(get_absolute_time());
}


int main() {
    set_log_function(log_fn);
    set_timestamp_function(timestamp_fn);

    setup_default_uart();

    printf("Hello, world %i!\n", infer(log_fn));
    return 0;
}
