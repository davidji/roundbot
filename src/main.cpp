
#define _USE_MATH_DEFINES

#include <functional>
#include <math.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include "mbed.h"
#include "motor.h"
#include "differential.h"
#include "hc-sr04.h"
#include "wiring.h"

const float pi = 3.1415927;
const float gearMotorRatio = 50.0;
const int encoderArms = 3;
const float wheelDiameter = 0.032;
const float wheelBase = 0.083;
const float stepLength = (pi*wheelDiameter)/(gearMotorRatio*encoderArms);

Serial console(D1, D0);

// Break/drive mode gives nice linear response, but the first 10% produces little to no movement.
motor::MotorOut leftMotor(motor_left_in1_pin, motor_left_in2_pin, BRAKE, 0.1, 1.0);
motor::MotorOut rightMotor(motor_right_in1_pin, motor_right_in2_pin, BRAKE, 0.1, 1.0);
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

void print_encoder_info() {
    console.printf("min(l1): %02d max(l1): %02d min(l2): %02d max(l2): %02d "
           "min(r1): %02d max(r1): %02d min(r2): %02d max(r2): %02d ",
           percent(leftEncoder.in1.minimum),
           percent(leftEncoder.in1.maximum),
           percent(leftEncoder.in2.minimum),
           percent(leftEncoder.in2.maximum),
           percent(rightEncoder.in1.minimum),
           percent(rightEncoder.in1.maximum),
           percent(rightEncoder.in2.minimum),
           percent(rightEncoder.in2.maximum));
}

void motorsTestStep(float left, float right) {
    testTimer.reset();
    leftEncoder.read();
    rightEncoder.read();
    drive(left, right);
    wait_ms(1000);
    led1 = ~led1;
    long left_rotation = differential.left.read()*1000;
    long right_rotation = differential.right.read()*1000;
    long s = testTimer.read_ms();
    console.printf("duty: %+04d, %+04d distance: %+06ld, %+06ld rate: %+06ld, %+06ld\n",
            percent(left),
            percent(right),
            left_rotation,
            right_rotation,
            left_rotation/s,
            right_rotation/s);
}

void motorsTest(float speed) {
    console.printf("motors test %f\n", speed);
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



void motorsTestSpeeds() {
    while(true) {
        for(int i = 1; i <= 4; ++i) {
            motorsTest(i*0.25);
        }
    }
}

void differential_test() {
    differential.start();

    // this little hack calibrates the encoders before we start the turns
    while (true) {
        differential.turn(pi/2.0);
        wait(3.0);
        differential.move(0.1);
        wait(3.0);
        led1.write(!led1.read());
    }
}

void encoder_test() {
    while (true) {
        motorsTestSpeeds();
    }
}

int mm(float m) {
    return m*1000;
}

void shell() {
    char buffer[40];
    char command[20];
    char arg[20];

    differential.start();
    while(true) {
        console.printf("ready\n");
        int i = 0;
        char c = console.getc();
        for(i = 0; i != sizeof(buffer) && c != '\n'; ++i) {
            buffer[i] = c;
            c = console.getc();
        }
        buffer[i] = '\0';

        int tokens = sscanf(buffer, " %20s %20s", command, arg);
        switch (tokens) {
        case 2: {
                float value = strtof(arg, NULL);
                if(value == 0.0) {
                    console.printf("error: could not parse argument as floating point %s\n", arg);
                } else if(strcmp("move", command) == 0) {
                    console.printf("move %dmm\n", mm(value));
                    differential.move(value);
                } else if(strcmp("turn", command) == 0) {
                    console.printf("turn %d\n", mm(value));
                    differential.turn(value);
                } else {
                    console.printf("error: unknown command %s\n", command);
                }
            }
            break;
        case 1:
            if(strcmp("range", command) == 0) {
                console.printf("range %dmm\n", mm(range.read()));
            } else if(strcmp("progress", command) == 0) {
                console.printf("progress left=%dmm, right=%dmm\n",
                        mm(differential.left.peek()), mm(differential.right.peek()));
            } else if(strcmp("test", command) == 0) {
                console.printf("test\n");
                motorsTestSpeeds();
            } else if(strcmp("calibrate", command) == 0) {
                testTimer.start();
                for(float duty = 0; duty <= 1.0; duty = duty + 0.01) {
                    motorsTestStep(duty, duty);
                }
                console.printf("encoders: ");
                print_encoder_info();
                console.printf("\n");
            } else {
                console.printf("error: unknown command %s\n", command);
            }
            break;
        default:
            console.printf("error: malformed command: %s\n", buffer);
        }
    }
}

int main() {
    console.baud(38400);
    console.printf("roundbot\n");
    range.start();
    led1 = true;

    // encoder_test();
    // differential_test();
    shell();
}
