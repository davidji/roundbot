
#include "motor.h"
#include <math.h>

namespace motor {

MotorOut::MotorOut(PinName out1pin, PinName out2pin, MotorMode initial_mode, float min, float max)
: out1(PwmOut(out1pin)), out2(PwmOut(out2pin)),
  min_duty(min), max_duty(max) {
    out1.period_us(2500);
    out2.period_us(2500);
    mode(initial_mode);
    switch(default_mode) {
    case BRAKE:
        brake();
    case FREE:
        free();
    }
}

void MotorOut::mode(MotorMode new_mode) {
    default_mode = new_mode == FREE ? FREE : BRAKE;
}

void MotorOut::free() {
    write(0.0, 0.0);
}

void MotorOut::brake() {
    write(1.0, 1.0);
}

void MotorOut::drive(float duty, MotorMode drive_mode) {
    float normalised = fabs(duty)*(max_duty - min_duty) + min_duty;
    switch(drive_mode) {
    case DEFAULT:
        drive(duty, default_mode);
        break;
    case FREE:
        if(duty < 0) {
            write(normalised, 0.0);
        } else if(duty > 0) {
            write(0.0, normalised);
        } else {
            free();
        }
        break;
    case BRAKE:
        if(duty < 0) {
            write(1.0 - normalised, 1.0);
        } else if(duty > 0) {
            write(1.0, 1.0 - normalised);
        } else {
            brake();
        }
        break;
    }
}

void MotorOut::write(float in1v, float in2v) {
    out1.write(in1v);
    out2.write(in2v);
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
  minimum(1.0),
  maximum(0.0)
  { }

inline bool MinMax::read() {
    float value = in.read();
    if(maximum < value || minimum > value) {
        minimum = fmin(value, minimum);
        maximum = fmax(value, maximum);
        zero = (minimum + maximum)/2;
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
    ticker.attach_us(Callback<void ()>(this, &MotorEncoder::sample), period_us);
}

void MotorEncoder::stop() {
    ticker.detach();
}

}; /* namespace motor */
