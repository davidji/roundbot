/*
 * DifferentialDrive.h
 *
 *  Created on: 28 Aug 2016
 *      Author: david
 */

#ifndef _DIFFERENTIAL_H_
#define _DIFFERENTIAL_H_

#include "motor.h"
#include "PID.h"

using motor::MotorOut;
using motor::MotorEncoder;
using motor::Direction;

class Wheel {
public:
    MotorOut &out;
private:
    MotorEncoder &encoder;

    /**
     * This is the distance on the circumference of the wheel for
     * one step of the encoder.
     */
    const float stepLength;

    void step(Direction);

public:
    Wheel(const Wheel &other);
    Wheel(MotorOut &_out, MotorEncoder &_encoder, float _stepLength);

    void start();
    float read();
    float peek();
};

class DifferentialDrive {
public:
    Wheel left, right;

private:

    /** The distance between the wheels */
    float length;

    /** This controller balances power between the two wheels, where
     *  the error is the difference in rotation rate.
     */
    PID balanceController;

    /** control the overall power during turning */
    PID turningController;

    Ticker ticker;

    static constexpr timestamp_t pid_period_us = 1000;
    static constexpr float pid_period = ((float)pid_period_us)/1000000.0;

    PID movingController;

    void turningTick(void);
    void movingTick(void);

public:
    DifferentialDrive(Wheel left, Wheel right, float length);
    void start();
    void turn(float radians);
    void move(float meters);
    const float pi = 3.1415927;
};

#endif /* _DIFFERENTIAL_H_ */
