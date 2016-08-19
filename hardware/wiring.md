
I'm using an STM32F303K8 Nucleo board for GPIO. It's functions are

 - PWM motor control (2 PWM, 4 GPIO)
 - rotary encoder feedback ADC channels 4
 - analog reflectance sensors ADC channels x3
 - ultrasonic rangefinder sensor Timer x1 one in channel, one out channel
 - status LED dislay Timer x1 one out channel
 - Serial interface to raspberry PI
 - NRF24 via SPI + 2GPIO

See https://developer.mbed.org/platforms/ST-Nucleo-F303K8/

Here are all the options for each pin

MCU  |MBED | Function
-----|-----|----------
PA9  | D1  | TSC_G4_IO1, TIM1_CH2, USART1_TX, TIM15_BKIN, TIM2_CH3
PA10 | D0  | TIM17_BKIN, TSC_G4_IO2, TIM1_CH3, USART1_RX, COMP6_OUT, TIM2_CH4
PA12 | D2  | TIM16_CH1, TIM1_CH2N, USART1_RTS_DE, COMP2_OUT, CAN_TX, TIM1_ETR
PB0  | D3  | TIM3_CH3, TSC_G3_IO2, TIM1_CH2N
PB7  | D4  | TIM17_CH1N, TSC_G5_IO4, I2C1_SDA, USART1_RX, TIM3_CH4
PB6  | D5  | TIM16_CH1N, TSC_G5_IO3, I2C1_SCL, USART1_TX
PB1  | D6  | TIM3_CH4, TSC_G3_IO3, TIM1_CH3N, COMP4_OUT
PF0  | D7  | TIM1_CH3N
PF1  | D8  |
PA8  | D9  | TIM1_CH1, USART1_CK
PA11 | D10 | TIM1_CH1N, USART1_CTS, CAN_RX, TIM1_CH4, TIM1_BKIN2
PB5  | D11 | TIM16_BKIN, TIM3_CH2, I2C1_SMBA, SPI1_MOSI, USART2_CK, TIM17_CH
PB4  | D12 | TIM16_CH1, TIM3_CH1, TSC_G5_IO2, SPI1_MISO, USART2_RX, TIM17_BKIN
PA2  | A7  | ADC1_IN3, COMP2_INM, TIM2_CH3, TSC_G1_IO3, USART2_TX, COMP2_OUT, TIM15_CH1
PA7  | A6  | ADC2_IN4, COMP2_INP, OPAMP2_VINP, TIM17_CH1, TIM3_CH2, TSC_G2_IO4, SPI1_MOSI, TIM1_CH1N
PA6  | A5  | ADC2_IN3, DAC2_OUT1, OPAMP2_VOUT, TIM16_CH1, TIM3_CH1, TSC_G2_IO3, SPI1_MISO, TIM1_BKIN
PA5  | A4  | ADC2_IN2, DAC1_OUT2, OPAMP2_VINM, TIM2_CH1/TI M2_ETR, TSC_G2_IO2, SPI1_SCK
PA4  | A3  | ADC2_IN1, DAC1_OUT1, COMP2_INM4, COMP4_INM4, COMP6_INM4, TIM3_CH2, TSC_G2_IO1, SPI1_NSS, USART2_CK
PA3  | A2  | ADC1_IN4, TIM2_CH4, TSC_G1_IO4, USART2_RX, TIM15_CH2
PA1  | A1  | ADC1_IN2, TIM2_CH2, TSC_G1_IO2, USART2_RTS_DE, TIM15_CH1N
PA0  | A0  | ADC1_IN1, TIM2_CH1/TI M2_ETR, TSC_G1_IO1, USART2_CTS
PB3  | D13 | SWO, TIM2_CH2, TSC_G5_IO1, SPI1_SCK, USART2_TX, TIM3_ETR, ADC2_IN12, COMP4_INM, TSC_G3_IO4

TIM2,TIM3: Motor control
TIM1: WS2812
ADC1: Rotary encoders
ADC2: Reflectance sensors
SPI1: RF24

MCU  | MBED| Function  | Used
-----|-----|-----------|----------
PA9  | D1  | USART1_TX | Serial TX
PA10 | D0  | USART1_RX | Serial RX
PA12 | D2  |           | Unused
PB0  | D3  | TIM1_CH2N | Motor L IN1
PB7  | D4  | I2C1_SDA  | I2C Raspberry Pi/other
PB6  | D5  | I2C1_SCL  | I2C Raspberry Pi/other
PB1  | D6  |           | Unused
PF0  | D7  | TIM1_CH3N | Motor L IN2
PF1  | D8  |           | Unused
PA8  | D9  | TIM1_CH1  | Motor R IN1
PA11 | D10 | TIM1_CH4  | Motor R IN2
PB5  | D11 | SPI_MOSI  | RF24 MOSI
PB4  | D12 | SPI_MISO  | RF24 MISO
PA2  | A7  |           | Unused
PA7  | A6  | ADC2_IN4  | Rotary encoder R2
PA6  | A5  | ADC2_IN3  | Rotary encoder R1
PA5  | A4  | ADC2_IN2  | Rotary encoder L2
PA4  | A3  | ADC2_IN1  | Rotary encoder L1
PA3  | A2  | ADC1_IN4  | Reflectance 3
PA1  | A1  | ADC1_IN2  | Reflectance 2
PA0  | A0  | ADC1_IN1  | Reflectance 1
PB3  | D13 | SPI1_SCK  | RF24 SCK

