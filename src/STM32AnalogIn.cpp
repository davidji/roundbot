/*
 * STM32AnalogIn.cpp
 *
 *  Created on: 15 Nov 2017
 *      Author: david
 */

#include <STM32AnalogIn.h>

bool STM32AnalogIn::_configure_channel(ADC_ChannelConfTypeDef &sConfig, uint32_t rank) {
    // Configure ADC channel
    sConfig.Rank = rank;
    sConfig.SamplingTime = _samplingTime;
    sConfig.SingleDiff = ADC_SINGLE_ENDED;
    sConfig.OffsetNumber = ADC_OFFSET_NONE;
    sConfig.Offset = 0;

	switch (_adc.channel) {
		case 1:
			sConfig.Channel = ADC_CHANNEL_1;
			break;
		case 2:
			sConfig.Channel = ADC_CHANNEL_2;
			break;
		case 3:
			sConfig.Channel = ADC_CHANNEL_3;
			break;
		case 4:
			sConfig.Channel = ADC_CHANNEL_4;
			break;
		case 5:
			sConfig.Channel = ADC_CHANNEL_5;
			break;
		case 6:
			sConfig.Channel = ADC_CHANNEL_6;
			break;
		case 7:
			sConfig.Channel = ADC_CHANNEL_7;
			break;
		case 8:
			sConfig.Channel = ADC_CHANNEL_8;
			break;
		case 9:
			sConfig.Channel = ADC_CHANNEL_9;
			break;
		case 10:
			sConfig.Channel = ADC_CHANNEL_10;
			break;
		case 11:
			sConfig.Channel = ADC_CHANNEL_11;
			break;
		case 12:
			sConfig.Channel = ADC_CHANNEL_12;
			break;
		case 13:
			sConfig.Channel = ADC_CHANNEL_13;
			break;
		case 14:
			sConfig.Channel = ADC_CHANNEL_14;
			break;
		case 15:
			sConfig.Channel = ADC_CHANNEL_15;
			break;
		case 16:
			sConfig.Channel = ADC_CHANNEL_16;
			break;
		case 17:
			sConfig.Channel = ADC_CHANNEL_17;
			break;
		case 18:
			sConfig.Channel = ADC_CHANNEL_18;
			break;
		default:
			return false;
	}

	return true;

}

uint16_t STM32AnalogIn::_read()
{
    ADC_ChannelConfTypeDef sConfig = {0};
    if(!_configure_channel(sConfig, ADC_REGULAR_RANK_1))
    	return 0;

	HAL_ADC_ConfigChannel(&_adc.handle, &sConfig);
	HAL_ADC_Start(&_adc.handle); // Start conversion

    // Wait end of conversion and get value
    if (HAL_ADC_PollForConversion(&_adc.handle, 10) == HAL_OK) {
        return (HAL_ADC_GetValue(&_adc.handle));
    } else {
        return 0;
    }
}

