#include "mbed.h"
#include "rtos.h"
#include "motor.h"
#include "wiring.h"

Motor left_motor(motor_left_en_pin, motor_left_in1_pin, motor_left_in2_pin);
Motor right_motor(motor_right_en_pin, motor_right_in1_pin, motor_right_in2_pin);

void drive(float left, float right) {
    left_motor.drive(left);
    right_motor.drive(right);
}

void motors_test_step(float left, float right) {
    drive(left, right);
    wait(1);
}

void motors_test(float speed) {
    motors_test_step(0.0, 0.0); //stop
    motors_test_step(speed, speed); // forward
    motors_test_step(-speed, -speed); // backward
    motors_test_step(speed, 0.0); // turn right
    motors_test_step(0.0, speed); // turn left
    motors_test_step(speed, -speed); // spin right
    motors_test_step(-speed, speed); // spin left
    motors_test_step(0.0, 0.0); //stop
}


int main() {
    while(true) {
        for(int i = 1; i <= 4; ++i) {
            motors_test(i*0.25);
        }
    }
}
