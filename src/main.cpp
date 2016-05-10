#include "mbed.h"
#include "rtos.h"
#include "Motor.h"

DigitalOut myled(LED1);

int main() {
    while(1) {
        myled = 1;
        wait(2);
        myled = 0;
        wait(1);
    }
}
