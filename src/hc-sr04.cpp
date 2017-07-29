
#include "hc-sr04.h"

HC_SR04::HC_SR04(PinName trig_pin, PinName echo_pin) : trig(trig_pin), echo(echo_pin) {
    echo.rise(callback(this, &HC_SR04::rise));
    echo.fall(callback(this, &HC_SR04::fall));
}

void HC_SR04::rise(void) {
    timer.start();
}

void HC_SR04::fall(void) {
    timer.stop();
    reading = timer.read_us()/5800.0;
    result = true;
}

void HC_SR04::trigger(void) {
    timer.stop();
    if(!result) {
        reading = NAN;
    }
    timer.reset();
    result = false;
    trig = true;
    wait_us(10);
    trig = false;
}

float HC_SR04::read() {
    return reading;
}

void HC_SR04::start() {
    ticker.attach_us(callback(this, &HC_SR04::trigger), 60000);
}

void HC_SR04::stop() {
    ticker.detach();
}
