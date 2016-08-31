/*
 * DifferentialDrive.cpp
 *
 *  Created on: 28 Aug 2016
 *      Author: david
 */

#include <differential.h>
#include <stdio.h>


Wheel::Wheel(const Wheel& other)
  : out(other.out), encoder(other.encoder), stepLength(other.stepLength) {
}

Wheel::Wheel(MotorOut& _out, MotorEncoder& _encoder, float _stepLength)
    : out(_out), encoder(_encoder), stepLength(_stepLength) {
    encoder.step(this, &Wheel::step);
}


DifferentialDrive::DifferentialDrive(Wheel _left, Wheel _right, float _length)
  :left(_left),
   right(_right),
   length(_length),
   balanceController(1.0, 0.0, 0.0, turning_period),
   turningController(2.0, 0.0, 0.001, turning_period)  {

    balanceController.setOutputLimits(0.5, 1.5);
    balanceController.setSetPoint(1.0);
    balanceController.setMode(AUTO_MODE);

    turningController.setOutputLimits(-1.0, +1.0);
    turningController.setMode(AUTO_MODE);
}

void DifferentialDrive::start() {
    left.start();
    right.start();
}

void DifferentialDrive::turn(float radians) {
    left.read();
    right.read();
    turningController.setSetPoint(radians);
    turningController.setInputLimits(radians-pi, radians+pi);
    turningController.reset();
    ticker.attach_us(this, &DifferentialDrive::turningTick, turning_period_us);
}

static int millis(float x) {
    return x*1000;
}

void DifferentialDrive::turningTick() {
    float right_turn = right.peek();
    float left_turn = left.peek();
    float value = (right_turn - left_turn) / length;
    turningController.setProcessValue(value);
    float output = turningController.compute();
    right.out.drive(+output);
    left.out.drive(-output);
}


void Wheel::step(motor::Direction direction) {

}

float Wheel::read() {
    float steps = encoder.read();
    return steps*stepLength;
}

void Wheel::start() {
    encoder.start();
}

float Wheel::peek() {
    float steps = encoder.peek();
    return steps*stepLength;
}
