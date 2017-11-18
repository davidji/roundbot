
#include <functional>
#include "mbed.h"
#include "STM32AnalogIn.h"

#ifndef _MOTOR_H_
#define _MOTOR_H_

typedef enum { FREE, BRAKE, DEFAULT } MotorMode;

namespace motor {

class MotorOut {
private:
    PwmOut out1;
    PwmOut out2;
    MotorMode default_mode;
    float min_duty;
    float max_duty;

    void write(float in1, float in2);

public:
    MotorOut(PinName out1, PinName out2, MotorMode mode = BRAKE, float min = 0.0, float max = 1.0);
    void mode(MotorMode mode);
    void free();
    void brake();
    void drive(float percent, MotorMode mode = DEFAULT);
};

class MinMax {

private:
    float zero;
public:
    const PinName pin;
    volatile float minimum;
    volatile float maximum;

    MinMax(PinName pin);
    bool update(float value);
};

typedef enum direction: int { FORWARD = 1, BACKWARD = -1 } Direction;

class MotorEncoder {

private:
    Ticker ticker;
    bool in1_prev_value = false;
    volatile long delta_r;

public:
    MinMax in1;
    MinMax in2;
    volatile long count_s;

    MotorEncoder(PinName in1, PinName in2);
    long read();
    long peek();
    void update(float in1, float in2);

};

}; /* namespace motor */


#endif
