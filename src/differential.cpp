/*
 * DifferentialDrive.cpp
 *
 *  Created on: 28 Aug 2016
 *      Author: david
 */

#include <differential.h>
#include <stdio.h>


Wheel::Wheel(const Wheel& other)
  : out(other.out), encoder(other.encoder),
	in1(other.encoder.in1.pin),
	in2(other.encoder.in2.pin),
	stepLength(other.stepLength) {
}

Wheel::Wheel(MotorOut& _out, MotorEncoder& _encoder, float _stepLength)
    : out(_out), encoder(_encoder),
	  in1(_encoder.in1.pin, ADC_SAMPLETIME_1CYCLE_5),
	  in2(_encoder.in2.pin, ADC_SAMPLETIME_1CYCLE_5),
	  stepLength(_stepLength) {
}


DifferentialDrive::DifferentialDrive(Wheel _left, Wheel _right, float _length)
  :left(_left),
   right(_right),
   length(_length),
   balanceController(1.0, 0.0, 0.0, pid_period),
   turningController(10.0, 0.0, 0.00001, pid_period),
   movingController(10.0, 0.0, 0.0, pid_period) {

    balanceController.setOutputLimits(0.5, 1.5);
    balanceController.setSetPoint(1.0);
    balanceController.setMode(AUTO_MODE);

    turningController.setOutputLimits(-0.75, +0.75);
    turningController.setMode(AUTO_MODE);

    movingController.setOutputLimits(-0.75, +0.75);
    movingController.setMode(AUTO_MODE);
}

void DifferentialDrive::start() {
	encodingTicker.attach_us(callback(this, &DifferentialDrive::encoderTick), encoder_period_us);
}

void DifferentialDrive::stop() {
	encodingTicker.detach();
	driveTicker.detach();
}

void DifferentialDrive::encoderTick() {
	left.encoder.update(left.in1.read(), left.in2.read());
	right.encoder.update(right.in1.read(), right.in2.read());
}

void DifferentialDrive::turn(float radians) {
    driveTicker.detach();
    left.read();
    right.read();
    turningController.setSetPoint(radians);
    turningController.setInputLimits(radians-pi, radians+pi);
    turningController.reset();
    driveTicker.attach_us(callback(this, &DifferentialDrive::turningTick), pid_period_us);
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

float Wheel::read() {
    float steps = encoder.read();
    return steps*stepLength;
}

float Wheel::peek() {
    float steps = encoder.peek();
    return steps*stepLength;
}

void DifferentialDrive::movingTick(void) {
    float right_turn = right.peek();
    float left_turn = left.peek();
    float value = (right_turn + left_turn) / 2;
    movingController.setProcessValue(value);
    float output = movingController.compute();
    right.out.drive(-output);
    left.out.drive(-output);
}

void DifferentialDrive::move(float meters) {
    driveTicker.detach();
    left.read();
    right.read();
    movingController.setSetPoint(meters);
    movingController.setInputLimits(meters-0.1, meters+0.1);
    movingController.reset();
    driveTicker.attach_us(callback(this, &DifferentialDrive::movingTick), pid_period_us);
}
