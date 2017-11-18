/*
 * STM32AnalogIn.h
 *
 *  Created on: 15 Nov 2017
 *      Author: david
 */

#ifndef SRC_STM32ANALOGIN_H_
#define SRC_STM32ANALOGIN_H_

#include <mbed.h>
#include <array>

template<unsigned int N>
class STM32AnalogInGroup;

class STM32AnalogIn : public AnalogIn {
    friend STM32AnalogInGroup;
public:

    /** Create an AnalogIn, connected to the specified pin
     *
     * @param pin AnalogIn pin to connect to
     */
    STM32AnalogIn(PinName pin, uint32_t samplingTime = ADC_SAMPLETIME_19CYCLES_5) : AnalogIn(pin), _samplingTime(samplingTime) { }

    void samplingTime(uint32_t samplingTime) {
    	_samplingTime = samplingTime;
    }

    /** Read the input voltage, represented as a float in the range [0.0, 1.0]
     *
     * @returns A floating-point value representing the current input voltage, measured as a percentage
     */
    float read() {
        unsigned short value = _read();
        return (float)value * (1.0f / (float)0xFFF);
    }

    /** Read the input voltage, represented as an unsigned short in the range [0x0, 0xFFFF]
     *
     * @returns
     *   16-bit unsigned short representing the current input voltage, normalised to a 16-bit value
     */
    unsigned short read_u16() {
        unsigned short ret = _read();
        return ret;
    }

    /** An operator shorthand for read()
     *
     * The float() operator can be used as a shorthand for read() to simplify common code sequences
     *
     * Example:
     * @code
     * float x = volume.read();
     * float x = volume;
     *
     * if(volume.read() > 0.25) { ... }
     * if(volume > 0.25) { ... }
     * @endcode
     */
    operator float() {
        // Underlying call is thread safe
        return read();
    }

    virtual ~STM32AnalogIn() {
        // Do nothing
    }

private:
    unsigned short _read();
    bool _configure_channel(ADC_ChannelConfTypeDef &sConfig, uint32_t rank);
    uint32_t _samplingTime;
};

bool adc_interrupt_init(ADC_HandleTypeDef &handle, unsigned int channels);

template<unsigned int N>
class STM32AnalogInGroup {
public:
	void attach_us(Callback<void (array<float,N>)> callback, long us) {
		
		ADC_HandleTypeDef &handle = inputs[0]._adc.handle;

		// Configure ADC
		handle.State = HAL_ADC_STATE_RESET;
	    handle.Init.ClockPrescaler        = ADC_CLOCKPRESCALER_PCLK_DIV2;
	    handle.Init.Resolution            = ADC_RESOLUTION12b;
	    handle.Init.DataAlign             = ADC_DATAALIGN_RIGHT;
	    handle.Init.ScanConvMode          = ENABLE;
	    handle.Init.EOCSelection          = EOC_SINGLE_CONV;
	    handle.Init.LowPowerAutoWait      = DISABLE;
	    handle.Init.ContinuousConvMode    = DISABLE;
	    handle.Init.NbrOfConversion       = N;
	    handle.Init.DiscontinuousConvMode = DISABLE;
	    handle.Init.NbrOfDiscConversion   = 0;
	    handle.Init.ExternalTrigConv      = ADC_SOFTWARE_START;
	    handle.Init.ExternalTrigConvEdge  = ADC_EXTERNALTRIGCONVEDGE_NONE;
	    handle.Init.DMAContinuousRequests = DISABLE;
	    handle.Init.Overrun               = OVR_DATA_OVERWRITTEN;

	    if (HAL_ADC_Init(&handle) != HAL_OK) {
	        error("Cannot initialize ADC");
	    }
		
		for(unsigned int i = 0; i != N; ++i) {
			ADC_ChannelConfTypeDef config;
			inputs[i]._configure_channel(config, ADC_REGULAR_RANK_1+i);
			HAL_ADC_ConfigChannel(&handle, &config);
		}

		ticker.attach_us(Callback(this, start), us);
	}

private:
	void start() {
		ADC_HandleTypeDef &handle = inputs[0]._adc.handle;
		HAL_ADC_Start_IT(&handle);
	}

	static void report() {

	}

	Ticker ticker;
    array<STM32AnalogIn, N> inputs;
    Callback<void (array<float,N>)> callback;

    static Callback<void(void)> completed;
};

#endif /* SRC_STM32ANALOGIN_H_ */
