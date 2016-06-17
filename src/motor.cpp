
#include "motor.h"
#include <math.h>

MotorOut::MotorOut(PinName enpin, PinName in1pin, PinName in2pin, MotorMode initial_mode)
: en(DigitalOut(enpin)), in1(PwmOut(in1pin)), in2(PwmOut(in2pin)) {
    in1.period_us(2500);
    in2.period_us(2500);
    mode(initial_mode);
    en.write(1);
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

void MotorOut::write(float in1v, float in2v) {
    in1.write(in1v);
    in2.write(in2v);
}



MotorEncoder::MotorEncoder(PinName in1pin, PinName in2pin)
: zero(0.25),
  in1(AnalogIn(in1pin)),
  in2(AnalogIn(in2pin)),
  ticker(),
  delta_r(0),
  count_s(0),
  min_v(1.0),
  max_v(0.0) {
}

void MotorEncoder::sample() {
    count_s++;
    float in1_next_value = in1.read();
    min_v = fmin(in1_next_value, min_v);
    max_v = fmax(in1_next_value, max_v);
    if(in1_prev_value < zero && in1_next_value > zero) {
        float in2_value = in2.read();
        delta_r += (in2_value > zero) ? 1 : -1;
    }

    in1_prev_value = in1_next_value;
}

long MotorEncoder::read() {
    long delta = delta_r;
    delta_r = 0;
    return delta;
}

long MotorEncoder::peek() {
    return delta_r;
}

void MotorEncoder::start() {
    ticker.attach_us(this, &MotorEncoder::sample, period_us);
}

void MotorEncoder::stop() {
    ticker.detach();
}
