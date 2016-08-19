#include "mbed.h"
#include "motor.h"
#include "hcsr04.h"
#include "wiring.h"

MotorOut leftMotor(motor_left_in1_pin, motor_left_in2_pin);
MotorOut rightMotor(motor_right_in1_pin, motor_right_in2_pin);
MotorEncoder leftEncoder(rotary_encoder_left_a_pin, rotary_encoder_left_b_pin);
MotorEncoder rightEncoder(rotary_encoder_right_a_pin, rotary_encoder_right_b_pin);

Timer testTimer;
DigitalOut led1(LED1);
HC_SR04 distance(distance_trig, distance_echo);

void drive(float left, float right) {
    leftMotor.drive(left);
    rightMotor.drive(right);
}

int percent(float f) {
    return f * 100.0f;
}

void motorsTestStep(float left, float right) {

    testTimer.reset();
    leftEncoder.read();
    rightEncoder.read();
    drive(left, right);
    wait_ms(1000);
    led1 = ~led1;
    long left_rotation = leftEncoder.read();
    long right_rotation = rightEncoder.read();
    long s = testTimer.read_ms();
    printf("speed: %+04d, %+04d rotation: %+06ld, %+06ld rate: %+06ld, %+06ld "
            "min(l1): %02d max(l1): %02d min(l2): %02d max(l2): %02d "
            "min(r1): %02d max(r1): %02d min(r2): %02d max(r2): %02d "
            "distance: %03d\n",
            percent(left),
            percent(right),
            left_rotation,
            right_rotation,
            (1000*left_rotation)/s,
            (1000*right_rotation)/s,
            percent(leftEncoder.in1.min),
            percent(leftEncoder.in1.max),
            percent(leftEncoder.in2.min),
            percent(leftEncoder.in2.max),
            percent(rightEncoder.in1.min),
            percent(rightEncoder.in1.max),
            percent(rightEncoder.in2.min),
            percent(rightEncoder.in2.max),
            percent(distance.read()));

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



int main() {
    printf("roundbot\n");
    distance.start();
    led1 = true;

    while (true) {
       motor_test_speeds();
    }
}
