#include "mbed.h"
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
    wait_ms(1000);
    long left_rotation = leftEncoder.read();
    long right_rotation = rightEncoder.read();
    long s = testTimer.read_ms();
    printf("rotation: %06ld, %06ld rate: %06ld, %06ld time: %09ld min: %02d max: %02d %09ld %09ld\n",
            left_rotation,
            right_rotation,
            left_rotation/s,
            right_rotation/s, s,
            (int)(rightEncoder.min_v*100.0f),
            (int)(rightEncoder.max_v*100.0f),
            leftEncoder.count_s,
            rightEncoder.count_s);
}

void motorsTest(float speed) {
    printf("motors test %f\n", speed);
    testTimer.start();
    leftEncoder.start();
    rightEncoder.start();
    motorsTestStep(0.0, 0.0); //stop
    motorsTestStep(speed, speed); // forward
    motorsTestStep(-speed, -speed); // backward
    motorsTestStep(speed, 0.0); // turn right
    motorsTestStep(0.0, speed); // turn left
    motorsTestStep(speed, -speed); // spin right
    motorsTestStep(-speed, speed); // spin left
    motorsTestStep(0.0, 0.0); //stop
    testTimer.stop();
    leftEncoder.stop();
    rightEncoder.stop();
}



void motor_test_speeds() {
    while(true) {
        for(int i = 1; i <= 4; ++i) {
            motorsTest(i*0.25);
        }
    }
}

DigitalOut led1(LED1);

int main() {
    printf("roundbot\n");
    led1 = true;

    while (true) {
        motor_test_speeds();
    }
}
