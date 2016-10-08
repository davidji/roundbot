
#include <functional>
#include "mbed.h"

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
    AnalogIn in;
    float zero;
public:
    volatile float minimum;
    volatile float maximum;

    MinMax(PinName in);
    bool read();
};

typedef enum direction: int { FORWARD = 1, BACKWARD = -1 } Direction;
typedef FunctionPointerArg1<void, Direction> StepFunctionPointer;

class MotorEncoder {

private:
    Ticker ticker;
    bool in1_prev_value = false;
    volatile long delta_r;
    Callback<void (Direction)> stepCallback;

    static constexpr timestamp_t period_us = 50;

public:
    MinMax in1;
    MinMax in2;
    volatile long count_s;

    MotorEncoder(PinName in1, PinName in2);
    void start();
    void stop();
    long read();
    long peek();
    void sample();

    /**
     * Attach a member function to be called by the encoder for each step
     * forward.
     *  @param tptr pointer to the object to call the member function on
     *  @param mptr pointer to the member function to be called
     */
    template<typename T>
    void step(T* tptr, void (T::*mptr)(Direction)) {
        stepCallback.attach(tptr, mptr);
    }
};

}; /* namespace motor */


#endif
