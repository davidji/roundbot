/*
 * ThreadTicker.h
 *
 *  Created on: 18 Oct 2016
 *      Author: david
 */

#ifndef SRC_DRIVERS_THREADTICKER_H_
#define SRC_DRIVERS_THREADTICKER_H_

#include "ch.hpp"

namespace mbed {

template<int N>
class ThreadTicker : private chibios_rt::BaseStaticThread<N> {
private:
	systime_t tick = TIME_IMMEDIATE;
	Callback tickFunction;

protected:
    virtual void main(void) {
    	systime_t time = chVTGetSystemTime();
        while (!this->shouldTerminate()) {
        	time += tick;
        	tickFunction();
        	this->sleepUntil(time);
        }
    }

public:
	ThreadTicker() { };

    void attach_us(Callback fn, long us) {
    	tickFunction = fn;
    	tick = US2ST(us);
    	this->start(HIGHPRIO);
    }

    void detach() {
    	if(this->thread_ref && !chThdTerminatedX(this->thread_ref)) {
    		this->requestTerminate();
    		this->wait();
    		tickFunction = Callback();
    	}
    };
};

} /* namespace mbed */
#endif /* SRC_DRIVERS_THREADTICKER_H_ */
