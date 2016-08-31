
#include <mbed.h>

#ifndef _HC_SR04_H_
#define _HC_SR04_H_

class HC_SR04 {
private:
    DigitalOut trig;
    InterruptIn echo;
    Timer timer;
    Ticker ticker;

    volatile float reading;
    volatile bool result;

    void trigger(void);
    void rise(void);
    void fall(void);

public:
    HC_SR04(PinName trig_pin, PinName echo_pin);

    void start();
    void stop();

    /**
     * Measure the distance to an object
     * @return distance in meters
     */
    float read();
};


#endif /* _HC_SR04_H_ */
