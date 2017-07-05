#include "mbed.h"

#ifdef TARGET_NUCLEO_F303K8
const PinName serial_tx_pin = D0;
const PinName serial_rx_pin = D1;
const PinName unused_D2 = D2;
const PinName motor_left_in1_pin = D3;
const PinName motor_left_in2_pin = D4;
const PinName motor_right_in1_pin = D5;
const PinName distance_trig = D6;
const PinName motor_right_in2_pin = D7;
const PinName distance_echo = D8;
const PinName unused_d9 = D9;
const PinName unused_d10 = D10;
const PinName rf24_mosi_pin = D11;
const PinName rf24_miso_pin = D12;
const PinName reflectance_3_pin = A2;
const PinName reflectance_2_pin = A1;
const PinName reflectance_1_pin = A0;
const PinName rf24_sck_pin = D13;

const PinName rotary_encoder_right_b_pin = A3;
const PinName rotary_encoder_right_a_pin = A4;
const PinName rotary_encoder_left_b_pin = A5;
const PinName rotary_encoder_left_a_pin = A6;
#endif

#ifdef TARGET_NUCLEO_F303RE
const PinName serial_tx_pin = PC_10;
const PinName serial_rx_pin = PC_11;
const PinName unused_D2 = D2;
const PinName motor_left_in1_pin = D3;
const PinName motor_left_in2_pin = D4;
const PinName motor_right_in1_pin = D5;
const PinName distance_trig = D6;
const PinName motor_right_in2_pin = D7;
const PinName distance_echo = D8;
const PinName unused_d9 = D9;
const PinName unused_d10 = D10;
const PinName rf24_mosi_pin = D11;
const PinName rf24_miso_pin = D12;
const PinName reflectance_3_pin = A2;
const PinName reflectance_2_pin = A1;
const PinName reflectance_1_pin = A0;
const PinName rf24_sck_pin = D13;

const PinName rotary_encoder_right_b_pin = PC_2;
const PinName rotary_encoder_right_a_pin = PC_3;
const PinName rotary_encoder_left_b_pin = PC_1;
const PinName rotary_encoder_left_a_pin = PC_0;
#endif

#ifdef TARGET_NUCLEO_L432KC
const PinName serial_tx_pin = D0;
const PinName serial_rx_pin = D1;
const PinName unused_D2 = D2;
const PinName motor_left_in1_pin = D3;
const PinName motor_left_in2_pin = D4;
const PinName motor_right_in1_pin = D5;
const PinName distance_trig = D6;
const PinName motor_right_in2_pin = D7;
const PinName distance_echo = D8;
const PinName unused_d9 = D9;
const PinName unused_d10 = D10;
const PinName rf24_mosi_pin = D11;
const PinName rf24_miso_pin = D12;
const PinName reflectance_3_pin = A2;
const PinName reflectance_2_pin = A1;
const PinName reflectance_1_pin = A0;
const PinName rf24_sck_pin = D13;

const PinName rotary_encoder_right_b_pin = A3;
const PinName rotary_encoder_right_a_pin = A4;
const PinName rotary_encoder_left_b_pin = A5;
const PinName rotary_encoder_left_a_pin = A6;
#endif
