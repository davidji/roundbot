
#include "mbed.h"

typedef enum { FREE, BRAKE, DEFAULT } MotorMode;

class Motor {
private:
    DigitalOut _en;
    PwmOut _in1;
    PwmOut _in2;
    MotorMode _mode;

    void write(float in1, float in2);

public:
    Motor(PinName en, PinName in1, PinName in2, MotorMode mode = BRAKE);
    void mode(MotorMode mode);
    void free();
    void brake();
    void drive(float percent, MotorMode mode = DEFAULT);
};

