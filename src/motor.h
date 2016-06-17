
#include "mbed.h"

typedef enum { FREE, BRAKE, DEFAULT } MotorMode;

class MotorOut {
private:
    DigitalOut en;
    PwmOut in1;
    PwmOut in2;
    MotorMode _mode;

    void write(float in1, float in2);

public:
    MotorOut(PinName en, PinName in1, PinName in2, MotorMode mode = BRAKE);
    void mode(MotorMode mode);
    void free();
    void brake();
    void drive(float percent, MotorMode mode = DEFAULT);
};

class MotorEncoder {
private:
    float zero;
    AnalogIn in1;
    AnalogIn in2;
    Ticker ticker;
    float in1_prev_value = 0.0;
    volatile long delta_r;

    static constexpr timestamp_t period_us = 50;

public:
    volatile long count_s;
    volatile float min_v;
    volatile float max_v;

    MotorEncoder(PinName in1, PinName in2);
    void start();
    void stop();
    long read();
    long peek();
    void sample();
};
