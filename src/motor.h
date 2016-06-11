
#include "mbed.h"

typedef enum { FREE, BRAKE, DEFAULT } MotorMode;

class MotorOut {
private:
    DigitalOut _en;
    PwmOut _in1;
    PwmOut _in2;
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
    InterruptIn _in1;
    DigitalIn _in2;
    long _delta_r;

    void trigger();

public:
    MotorEncoder(PinName in1, PinName in2);
    long read();
    long peek();
};
