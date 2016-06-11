
#include "motor.h"
#include <math.h>

MotorOut::MotorOut(PinName en, PinName in1, PinName in2, MotorMode initial_mode)
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

void MotorOut::mode(MotorMode mode) {
    _mode = mode == FREE ? FREE : BRAKE;
}

void MotorOut::free() {
    write(0.0, 0.0);
}

void MotorOut::brake() {
    write(1.0, 1.0);
}

void MotorOut::drive(float percent, MotorMode drive_mode) {
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

void MotorOut::write(float in1, float in2) {
    _in1.write(in1);
    _in2.write(in2);
}

void MotorEncoder::trigger() {
    if(_in2.read()) {
        _delta_r++;
    } else {
        _delta_r--;
    }
}

MotorEncoder::MotorEncoder(PinName in1, PinName in2)
: _in1(InterruptIn(in2)), _in2(DigitalIn(in1)) {
    _in1.rise(this, &MotorEncoder::trigger);
    _delta_r = 0;
}

long MotorEncoder::read() {
    long delta = _delta_r;
    _delta_r = 0;
    return delta;
}

long MotorEncoder::peek() {
    return _delta_r;
}
