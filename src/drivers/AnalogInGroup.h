/*
 * AnalogGroup.h
 *
 *  Created on: 16 Oct 2016
 *      Author: david
 */

#ifndef SRC_DRIVERS_ANALOGINGROUP_H_
#define SRC_DRIVERS_ANALOGINGROUP_H_

#include "mbed.h"
#include "assert.h"
#include "Ticker.h"

#define ADC_CFGR_DISCNUMC(channels) ((uint32_t)((channels+1)<<17))

namespace mbed {

typedef enum {
#if STM32_ADC_USE_ADC1 == TRUE
	ANALOG_IN_1,
#endif
#if STM32_ADC_USE_ADC2 == TRUE
	ANALOG_IN_2
#endif
} AnalogInDevice;

struct AnalogInChannel {
public:
	const PinName pin;
	const AnalogInDevice device;
	const unsigned int channel;
	constexpr AnalogInChannel(
			PinName pin,
			AnalogInDevice device,
			unsigned int channel) : pin(pin), device(device), channel(channel) {}
};



template<AnalogInDevice D>
constexpr ADC_HandleTypeDef *analogInDriver();

template <PinName P2>
constexpr AnalogInChannel analogInChannel();

#if STM32_ADC_USE_ADC1 == TRUE
template<> constexpr AnalogInChannel analogInChannel<A0>() { return AnalogInChannel(A0, ANALOG_IN_1, 1); }
template<> constexpr AnalogInChannel analogInChannel<A1>() { return AnalogInChannel(A1, ANALOG_IN_1, 2); }
template<> constexpr AnalogInChannel analogInChannel<A7>() { return AnalogInChannel(A7, ANALOG_IN_1, 3); }
template<> constexpr AnalogInChannel analogInChannel<A2>() { return AnalogInChannel(A2, ANALOG_IN_1, 4); }
template<> constexpr ADCDriver *analogInDriver<ANALOG_IN_1>() { return &ADCD1; }
#endif

#if (STM32_ADC_USE_ADC2 == TRUE ) || ((STM32_ADC_USE_ADC1 == TRUE) && (STM32_ADC_DUAL_MODE == TRUE))
template<> constexpr AnalogInChannel analogInChannel<A3>() { return AnalogInChannel(A3, ANALOG_IN_2, 1); }
template<> constexpr AnalogInChannel analogInChannel<A4>() { return AnalogInChannel(A4, ANALOG_IN_2, 2); }
template<> constexpr AnalogInChannel analogInChannel<A5>() { return AnalogInChannel(A5, ANALOG_IN_2, 3); }
template<> constexpr AnalogInChannel analogInChannel<A6>() { return AnalogInChannel(A6, ANALOG_IN_2, 4); }
template<> constexpr ADCDriver *analogInDriver<ANALOG_IN_2>() { return &ADCD2; }
#endif

template <AnalogInDevice D>
constexpr AnalogInDevice analogInDevice() { return D; };

template <AnalogInDevice D1, AnalogInDevice D2, AnalogInDevice ... DR >
constexpr AnalogInDevice analogInDevice() {
	static_assert(D1 == analogInDevice<D2, DR...>(), "All pins must refer to the same device");
	return D1;
};


template <
	unsigned int N,
	unsigned int C1 = 0,
	unsigned int C2 = 0,
	unsigned int C3 = 0,
	unsigned int C4 = 0,
	unsigned int C5 = 0,
	unsigned int ... C>
struct SQRn {
	static constexpr uint32_t value() {
		return SQRn<N-1, C ...>::value();
	}
};

template<
	unsigned int C1,
	unsigned int C2,
	unsigned int C3,
	unsigned int C4,
	unsigned int C5>
struct SQRn<0, C1, C2, C3, C4, C5> {
	static uint32_t value() {
		return (C1 | (C2<<6) | (C3<<12) | (C4<<18) | (C5<<24));
	}
};

template<int N, PinName ... P>
uint32_t SQR() {
	return SQRn<N, sizeof...(P) - 1, analogInChannel<P>().channel ...>::value();
}

template<PinName ... P>
class AnalogInGroup {
public:
	typedef enum {
		STOPPED, STARTING, IDLE, CONVERTING, CALLBACK, ERROR
	} State;


private:
	static constexpr uint32_t defaultSampleTime = ADC_SMPR_SMP_4P5;
	static AnalogInGroup *instance;
	static adcerror_t error;
	static uint32_t counter;
	static State state;

	static void endCallback(ADCDriver *adcp, adcsample_t *buffer, size_t n) {
		(void)adcp;
		(void)buffer;
		(void)n;
		if(state == CONVERTING) {
			counter++;
			state = CALLBACK;
			instance->completed();
			state = IDLE;
		}
	}

	static void errCallback(ADCDriver *adcp, adcerror_t err) {
		(void)adcp;
		error = err;
		state = IDLE;
	}

	ADCDriver *driver;
	ADCConversionGroup conversion = {
		false,
		sizeof...(P),
		endCallback,
		errCallback,
		/* cfgr  */ 0,
		/* tr1   */ 0,
#if STM32_ADC_DUAL_MODE
		/* ccr   */ 0,
#endif
		/* smpr  */ {
				ADC_SMPR1_SMP_AN1(defaultSampleTime) |
				ADC_SMPR1_SMP_AN2(defaultSampleTime) |
				ADC_SMPR1_SMP_AN3(defaultSampleTime) |
				ADC_SMPR1_SMP_AN4(defaultSampleTime) |
				ADC_SMPR1_SMP_AN5(defaultSampleTime) |
				ADC_SMPR1_SMP_AN6(defaultSampleTime) |
				ADC_SMPR1_SMP_AN7(defaultSampleTime) |
				ADC_SMPR1_SMP_AN8(defaultSampleTime) |
				ADC_SMPR1_SMP_AN9(defaultSampleTime),
				ADC_SMPR2_SMP_AN10(defaultSampleTime) |
				ADC_SMPR2_SMP_AN11(defaultSampleTime) |
				ADC_SMPR2_SMP_AN12(defaultSampleTime) |
				ADC_SMPR2_SMP_AN13(defaultSampleTime) |
				ADC_SMPR2_SMP_AN14(defaultSampleTime) |
				ADC_SMPR2_SMP_AN15(defaultSampleTime) |
				ADC_SMPR2_SMP_AN16(defaultSampleTime) |
				ADC_SMPR2_SMP_AN17(defaultSampleTime) |
				ADC_SMPR2_SMP_AN18(defaultSampleTime)
		},
		/* sqr   */ { SQR<0, P ...>(), SQR<1, P ...>(), SQR<2, P ...>(), SQR<3, P ...>() },
#if STM32_ADC_DUAL_MODE
		/* ssmpr */ {
				ADC_SMPR1_SMP_AN1(defaultSampleTime) |
				ADC_SMPR1_SMP_AN2(defaultSampleTime) |
				ADC_SMPR1_SMP_AN3(defaultSampleTime) |
				ADC_SMPR1_SMP_AN4(defaultSampleTime) |
				ADC_SMPR1_SMP_AN5(defaultSampleTime) |
				ADC_SMPR1_SMP_AN6(defaultSampleTime) |
				ADC_SMPR1_SMP_AN7(defaultSampleTime) |
				ADC_SMPR1_SMP_AN8(defaultSampleTime) |
				ADC_SMPR1_SMP_AN9(defaultSampleTime),
				ADC_SMPR2_SMP_AN10(defaultSampleTime) |
				ADC_SMPR2_SMP_AN11(defaultSampleTime) |
				ADC_SMPR2_SMP_AN12(defaultSampleTime) |
				ADC_SMPR2_SMP_AN13(defaultSampleTime) |
				ADC_SMPR2_SMP_AN14(defaultSampleTime) |
				ADC_SMPR2_SMP_AN15(defaultSampleTime) |
				ADC_SMPR2_SMP_AN16(defaultSampleTime) |
				ADC_SMPR2_SMP_AN17(defaultSampleTime) |
				ADC_SMPR2_SMP_AN18(defaultSampleTime)
		},
		/* ssqr  */ { 0, 0, 0, 0 }
#endif
	};

	static const PinName pins[sizeof...(P)];
	static constexpr AnalogInDevice device = analogInDevice<analogInChannel<P>().device ...>();
	static constexpr float sampleMaxValue =  0xfff.0p0;

	// this is the first field, because in the callback
	// we get a pointer to the buffer, which will be a
	// pointer to the object, and hence useful in general
	adcsample_t buffer[sizeof...(P)];


	Ticker ticker;
	Callback completed;

	void tickerStartConversion() {
		chSysLockFromISR();
		if(state == IDLE) {
			state = CONVERTING;
			adcStartConversionI(driver, &conversion, buffer, 1);
		}
		chSysUnlockFromISR();
	}

	bool transition(State from, State to) {
		chSysLock();
		if(state == from) {
			state = to;
			chSysUnlock();
			return true;
		} else {
			state = ERROR;
			chSysUnlock();
			return false;
		}
	}

public:
	AnalogInGroup() : driver(analogInDriver<device>()), ticker(), completed() {
	}

	void attach_us(Callback fn, long us) {
		if(transition(STOPPED, STARTING)) {
			completed = fn;
			instance = this;
			adcStart(driver, nullptr);

			for(int p = 0; p != sizeof...(P); ++p) {
				palSetPadMode(chibios::port(pins[p]), chibios::pad(pins[p]), PAL_MODE_INPUT_ANALOG);
			}

			transition(STARTING, IDLE);
			ticker.attach_us(Callback(this, &AnalogInGroup<P ...>::tickerStartConversion), us);
		}
	}

	void detach() {
		if(state != STOPPED) {
			ticker.detach();
		}

	}

	float read(int channel) {
		return ((float)buffer[channel])/sampleMaxValue;
	}

	int groupConversions() {
		return counter;
	}

	State groupState() {
		return state;
	}

};

template<PinName ... P>
AnalogInGroup<P ...> *AnalogInGroup<P ...>::instance;

template<PinName ... P>
const PinName AnalogInGroup<P ...>::pins[sizeof...(P)] = { analogInChannel<P>().pin ... };

template<PinName ... P>
adcerror_t AnalogInGroup<P ...>::error;

template<PinName ... P>
typename AnalogInGroup<P ...>::State AnalogInGroup<P ...>::state = STOPPED;

template<PinName ... P>
uint32_t AnalogInGroup<P ...>::counter = 0;

} /* namespace mbed */

#endif /* SRC_DRIVERS_ANALOGINGROUP_H_ */
