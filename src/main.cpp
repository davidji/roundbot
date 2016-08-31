
#define _USE_MATH_DEFINES

#include <functional>
#include <math.h>
#include "mbed.h"
#include "motor.h"
#include "differential.h"
#include "hc-sr04.h"
#include "wiring.h"

const float pi = 3.1415927;
const float gearMotorRatio = 50.0;
const int encoderArms = 3;
const float wheelDiameter = 0.032;
const float wheelBase = 0.084;
const float stepLength = (pi*wheelDiameter)/(gearMotorRatio*encoderArms);

motor::MotorOut leftMotor(motor_left_in1_pin, motor_left_in2_pin);
motor::MotorOut rightMotor(motor_right_in1_pin, motor_right_in2_pin);
motor::MotorEncoder leftEncoder(rotary_encoder_left_a_pin, rotary_encoder_left_b_pin);
motor::MotorEncoder rightEncoder(rotary_encoder_right_a_pin, rotary_encoder_right_b_pin);

DifferentialDrive differential(Wheel(leftMotor, leftEncoder, stepLength), Wheel(rightMotor, rightEncoder, stepLength), wheelBase);

Timer testTimer;
DigitalOut led1(LED1);
HC_SR04 range(distance_trig, distance_echo);

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
            percent(range.read()));

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

void differential_test() {
    differential.start();

    // this little hack calibrates the encoders before we start the turns
    testTimer.start();
    motorsTestStep(+0.25, -0.25);

    while (true) {
        differential.turn(pi/2.0);
        printf("waiting...\n");
        wait(10.0);
        led1.write(!led1.read());
    }
}

void encoder_test() {
    while (true) {
        motor_test_speeds();
    }
}

int main() {
    printf("roundbot\n");
    // range.start();
    led1 = true;

    // encoder_test();
    differential_test();
}
