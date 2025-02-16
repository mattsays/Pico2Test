#include <stdint.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

extern void    setLogFunction(void (*log_function)(uint8_t *string));
extern void    matmul_and_info(void);
extern size_t  get_last_result_size(void);
extern float   get_last_result(size_t index);

static void log_fn(uint8_t *string) {
    printf("%s\n", string);
}

int main() {
    stdio_init_all();   // Initialize USB and UART
    
    // Wait for USB CDC to be ready
    sleep_ms(5000);     // Increased delay to ensure USB is ready
    
    printf("Starting program...\n");
    sleep_ms(100);      // Small delay between prints
    
    setLogFunction(log_fn);
    
    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    
    printf("Entering main loop...\n");
    sleep_ms(100);      // Small delay between prints
    
    while (true) {
        gpio_put(LED_PIN, 1);
        printf("LED ON - Running matrix multiplication...\n");
        sleep_ms(500);
        
        matmul_and_info();
        
        // Print the actual results
        printf("Matrix multiplication result size: %zu\n", get_last_result_size());
        for (size_t i = 0; i < get_last_result_size(); i++) {
            printf("Result[%zu] = %f\n", i, get_last_result(i));
            sleep_ms(50);   // Small delay between prints
        }
        
        gpio_put(LED_PIN, 0);
        printf("LED OFF\n");
        sleep_ms(500);
    }

    return 0;
}
