
#include "motor.h"
#include <math.h>


MotorOut::MotorOut(PinName in1pin, PinName in2pin, MotorMode initial_mode)
: in1(PwmOut(in1pin)), in2(PwmOut(in2pin)) {
    in1.period_us(2500);
    in2.period_us(2500);
    mode(initial_mode);
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
            write(1.0 - fabs(percent), 1.0);
        } else {
            write(1.0, 1.0 - fabs(percent));
        }
        break;
    }
}

void MotorOut::write(float in1v, float in2v) {
    in1.write(in1v);
    in2.write(in2v);
}



MotorEncoder::MotorEncoder(PinName in1pin, PinName in2pin)
: ticker(),
  delta_r(0),
  in1(in1pin),
  in2(in2pin),
  count_s(0) {

}

MinMax::MinMax(PinName inpin)
: in(AnalogIn(inpin)),
  zero(0.5),
  min(1.0),
  max(0.0)
  { }

inline bool MinMax::read() {
    float value = in.read();
    if(max < value || min > value) {
        min = fmin(value, min);
        max = fmax(value, max);
        zero = (min + max)/2;
    }
    return value > zero;
}

void MotorEncoder::sample() {
    count_s++;
    bool in1_next_value = in1.read();
    if(!in1_prev_value && in1_next_value) {
        bool in2_value = in2.read();
        delta_r += in2_value ? 1 : -1;
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
