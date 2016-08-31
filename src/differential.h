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
private:
    Wheel left, right;

    /** The distance between the wheels */
    float length;

    /** This controller balances power between the two wheels, where
     *  the error is the difference in rotation rate.
     */
    PID balanceController;

    /** control the overall power during turning */
    PID turningController;
    Ticker ticker;

    static constexpr timestamp_t turning_period_us = 1000;
    static constexpr float turning_period = ((float)turning_period_us)/1000000.0;

    void turningTick(void);

public:
    DifferentialDrive(Wheel left, Wheel right, float length);
    void start();
    void turn(float radians);
    const float pi = 3.1415927;
};


#endif /* _DIFFERENTIAL_H_ */
