#include "mbed.h"
#include "rtos.h"
#include "motor.h"
#include "wiring.h"

MotorOut leftMotor(motor_left_en_pin, motor_left_in1_pin, motor_left_in2_pin);
MotorOut rightMotor(motor_right_en_pin, motor_right_in1_pin, motor_right_in2_pin);
MotorEncoder leftEncoder(rotary_encoder_left_a_pin, rotary_encoder_left_b_pin);
MotorEncoder rightEncoder(rotary_encoder_right_a_pin, rotary_encoder_right_b_pin);

Timer testTimer;

void drive(float left, float right) {
    leftMotor.drive(left);
    rightMotor.drive(right);
}

void motorsTestStep(float left, float right) {
    testTimer.reset();
    leftEncoder.read();
    rightEncoder.read();
    drive(left, right);
    wait(1);
    long left_rotation = leftEncoder.read();
    long right_rotation = rightEncoder.read();
    long s = testTimer.read_ms();
    printf("rotation: %06ld, %06ld rate: %d, %d time: %ld\n",
            left_rotation,
            right_rotation,
            (int)(left_rotation/s),
            (int)right_rotation/s, s);
}

void motors_test(float speed) {
    testTimer.start();
    printf("motors test\r\n");
    motorsTestStep(0.0, 0.0); //stop
    motorsTestStep(speed, speed); // forward
    motorsTestStep(-speed, -speed); // backward
    motorsTestStep(speed, 0.0); // turn right
    motorsTestStep(0.0, speed); // turn left
    motorsTestStep(speed, -speed); // spin right
    motorsTestStep(-speed, speed); // spin left
    motorsTestStep(0.0, 0.0); //stop
    testTimer.stop();
}


int main() {
    while(true) {
        for(int i = 1; i <= 4; ++i) {
            motors_test(i*0.25);
        }
    }
}
