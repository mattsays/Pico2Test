#include <stdint.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/time.h"

extern void    setLogFunction(void (*log_function)(uint8_t *string));
extern void    matmul_and_info(void);
extern size_t  get_last_result_size(void);
extern float   get_last_result(size_t index);

// Add predict function declaration
extern void predict(float* input, uint32_t* input_shape, uint32_t shape_len, float** result);

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

    // Test input data (5 values)
    float test_input[] = {0.1f, -10.0f, 5000.0f, 0.4f, 0.5f};
    uint32_t input_shape[] = {5}; // Shape is [5]
    float* result;
    
    while (true) {
        gpio_put(LED_PIN, 1);
        printf("LED ON - Running neural network prediction...\n");
        
        // Measure prediction time
        absolute_time_t start_time = get_absolute_time();
        predict(test_input, input_shape, 1, &result);
        absolute_time_t end_time = get_absolute_time();
        int64_t diff_us = absolute_time_diff_us(start_time, end_time);
        
        // Print timing and predictions
        printf("Prediction took %lld microseconds\n", diff_us);
        printf("Neural network predictions:\n");
        for (int i = 0; i < 5; i++) {
            printf("Class %d probability: %f\n", i, result[i]);
            sleep_ms(10);
        }
        
        gpio_put(LED_PIN, 0);
        printf("LED OFF\n");
        sleep_ms(10);
    }

    return 0;
}
