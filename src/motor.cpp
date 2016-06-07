
#include "motor.h"
#include <math.h>

Motor::Motor(PinName en, PinName in1, PinName in2, MotorMode initial_mode)
: _en(DigitalOut(en)), _in1(PwmOut(in1)), _in2(PwmOut(in2)) {
    _in1.period_us(2500);
    _in2.period_us(2500);
    mode(initial_mode);
    _en.write(1);
    switch(_mode) {
    case BRAKE:
        brake();
    case FREE:
        free();
    }
}

void Motor::mode(MotorMode mode) {
    _mode = mode == FREE ? FREE : BRAKE;
}

void Motor::free() {
    write(0.0, 0.0);
}

void Motor::brake() {
    write(1.0, 1.0);
}

void Motor::drive(float percent, MotorMode drive_mode) {
    switch(drive_mode) {
    case DEFAULT:
        drive(percent, _mode);
        break;
    case FREE:
        if(percent < 0) {
            write(fabs(percent), 0.0);
        } else {
            write(0.0, fabs(percent));
        }
        break;
    case BRAKE:
        if(percent < 0) {
            write(fabs(percent), 1.0);
        } else {
            write(1.0, fabs(percent));
        }
        break;
    }
}

void Motor::write(float in1, float in2) {
    _in1.write(in1);
    _in2.write(in2);
}
