
#ifndef PIN_NAMES_H
#define PIN_NAMES_H

#include <ch.h>
#include <hal.h>

#ifdef __cplusplus
extern "C" {
#endif

namespace mbed {

#if defined(BOARD_ST_NUCLEO32_F303K8)
typedef enum {
    D0  = 0x00,
    D1  = 0x01,
    D2  = 0x02,
    D3  = 0x03,
    D4  = 0x04,
    D5  = 0x05,
    D6  = 0x06,
    D7  = 0x07,
    D8  = 0x08,
    D9  = 0x09,
    D10 = 0x0A,
    D11 = 0x0B,
    D12 = 0x0C,
    D13 = 0x0D,
    A0  = 0x0E,
    A1  = 0x0F,
    A2  = 0x10,
    A3  = 0x11,
    A4  = 0x12,
    A5  = 0x13,
    A6  = 0x14,
    A7  = 0x15,

    LED1        = D13,
    SERIAL_TX   = D1,
    SERIAL_RX   = D0,
    USBTX       = D1,
    USBRX       = D0,
    I2C_SCL     = D4,
    I2C_SDA     = D5,
    SPI_MOSI    = D5,
    SPI_MISO    = D11,
    SPI_SCK     = D12,
    SPI_CS      = D13,

    NC = 0xff
}  PinName;
#elif defined(BOARD_ST_NUCLEO64_F303RE)
D0  = 0x00,
D1  = 0x01,
D2  = 0x02,
D3  = 0x03,
D4  = 0x04,
D5  = 0x05,
D6  = 0x06,
D7  = 0x07,
D8  = 0x08,
D9  = 0x09,
D10 = 0x0A,
D11 = 0x0B,
D12 = 0x0C,
D13 = 0x0D,
A0  = 0x0E,
A1  = 0x0F,
A2  = 0x10,
A3  = 0x11,
A4  = 0x12,
A5  = 0x13,
A6  = 0x14,
A7  = 0x15,

LED1        = D13,
SERIAL_TX   = D1,
SERIAL_RX   = D0,
USBTX       = D1,
USBRX       = D0,
I2C_SCL     = D15,
I2C_SDA     = D14,
SPI_MOSI    = D11,
SPI_MISO    = D12,
SPI_SCK     = D13,


NC = 0xff
}  PinName;
#endif

typedef enum {
    PIN_INPUT,
    PIN_OUTPUT
} PinDirection;

typedef enum {
    PullUp = 2,
    PullDown = 1,
    PullNone = 0,
    Repeater = 3,
    OpenDrain = 4,
    PullDefault = PullDown
} PinMode;

} /* namespace mbed */
#ifdef __cplusplus
}
#endif

#endif /* PIN_NAMES_H */
