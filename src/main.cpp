
#define _USE_MATH_DEFINES

#include <functional>
#include <math.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include "mbed.h"
#include "motor.h"
#include "differential.h"
#include "VL53L0X.h"

#include "Spki.h"
#include "CanonicalInput.h"
#include "FloatPair.h"
#include "Tag.h"
#include "TagDispatcher.h"
#include "SlipInput.h"
#include "SlipOutput.h"
#include "MBedStreamWrapper.h"

#include "wiring.h"

using namespace sexps;
using namespace slip;
using namespace motor;

Serial serial(SERIAL_TX, SERIAL_RX, 115200);
MBedStreamWrapper serialwrapper(serial);
SlipInput requests(serialwrapper);
SlipOutput responses(serialwrapper);


const float pi = 3.1415927;
const float gearMotorRatio = 50.0;
const int encoderArms = 3;
const float wheelDiameter = 0.032;
const float wheelBase = 0.083;
const float stepLength = (pi*wheelDiameter)/(gearMotorRatio*encoderArms);

Serial console(serial_tx_pin, serial_rx_pin);

// Break/drive mode gives nice linear response, but the first 10% produces little to no movement.
MotorOut leftMotor(motor_left_in1_pin, motor_left_in2_pin, BRAKE, 0.1, 1.0);
MotorOut rightMotor(motor_right_in1_pin, motor_right_in2_pin, BRAKE, 0.1, 1.0);
MotorEncoder leftEncoder(rotary_encoder_left_a_pin, rotary_encoder_left_b_pin);
MotorEncoder rightEncoder(rotary_encoder_right_a_pin, rotary_encoder_right_b_pin);

DifferentialDrive differential(Wheel(leftMotor, leftEncoder, stepLength), Wheel(rightMotor, rightEncoder, stepLength), wheelBase);

Timer testTimer;
DigitalOut led1(LED1);
I2C i2c(D4, D5);
Timer rangeTimer;
VL53L0X range(&i2c, &rangeTimer);
// APDS9960 gesture(i2c);


void drive(float left, float right) {
    leftMotor.drive(left);
    rightMotor.drive(right);
}

int percent(float f) {
    return f * 100.0f;
}

CanonicalOutput &operator<<(CanonicalOutput &out, motor::MinMax &in) {
	out << tag("min", in.minimum);
	out << tag("max", in.maximum);
	return out;
}

CanonicalOutput &operator<<(CanonicalOutput &out, MotorEncoder &encoder) {
	out << encoder.in1;
	out << encoder.in2;
	return out;
}

CanonicalOutput &operator<<(CanonicalOutput &out, DifferentialDrive &d) {
	float left = d.left.peek();
	float right = d.right.peek();
	out << tag("left", left);
	out << tag("right", right);
	return out;
}

void motorsTestStep(float left, float right) {
    testTimer.reset();
    leftEncoder.read();
    rightEncoder.read();
    drive(left, right);
    wait_ms(1000);
    led1 = ~led1;
    float left_rotation = differential.left.read();
    float right_rotation = differential.right.read();
    float s = testTimer.read();

    responses.begin();
    CanonicalOutput out(responses);
    out << '(' << "test";
    out << '(' << "parameters";
    out << tag("left", left);
    out << tag("right", right);
    out << ')';
    out << tag("left", left_rotation);
    out << tag("right", right_rotation);
    out << tag("time", s);
    out << ')';
    responses.end();
}

void motorsTest(float speed) {
    testTimer.start();
    leftEncoder.start();
    rightEncoder.start();
    motorsTestStep(0.0, 0.0); //stop
    motorsTestStep(speed, speed); // forward
    motorsTestStep(-speed, -speed); // backward
    motorsTestStep(speed, 0.0); // turn right
    motorsTestStep(0.0, speed); // turn left
    motorsTestStep(speed, -speed); // spin right
    motorsTestStep(-speed, speed); // spin left
    motorsTestStep(0.0, 0.0); //stop
    testTimer.stop();
    leftEncoder.stop();
    rightEncoder.stop();
}



void motorsTestSpeeds() {
    while(true) {
        for(int i = 1; i <= 4; ++i) {
            motorsTest(i*0.25);
        }
    }
}

void differential_test() {
    differential.start();

    // this little hack calibrates the encoders before we start the turns
    while (true) {
        differential.turn(pi/2.0);
        wait(3.0);
        differential.move(0.1);
        wait(3.0);
        led1.write(!led1.read());
    }
}

void encoder_test() {
    while (true) {
        motorsTestSpeeds();
    }
}

int mm(float m) {
    return m*1000;
}

class Shell {

public:

	bool invalid() {
		return false;
	}

	bool move(FloatPair &value) {
		differential.move(value);
		return true;
	}

	bool turn(FloatPair &value) {
		differential.turn(value);
		return true;
	}

	bool status() {
        responses.begin();
		CanonicalOutput out(responses);
		out << tag("progress", differential);
		responses.end();
        return true;
	}

	bool test() {
        motorsTestSpeeds();
        return true;
	}

	bool calibrate() {
        testTimer.start();
        for(float duty = 0; duty <= 1.0; duty = duty + 0.01) {
            motorsTestStep(duty, duty);
        }

        responses.begin();
		CanonicalOutput out(responses);
    	out << '(' << "encoders";
    	out << leftEncoder;
    	out << rightEncoder;
    	out << ')';
    	responses.end();

        return true;
	}


};

const auto dispatch = dispatcher(
		&Shell::invalid,
		tag("move", &Shell::move),
		tag("turn", &Shell::turn),
		tag("status", &Shell::status),
		tag("test", &Shell::test),
		tag("calibrate", &Shell::calibrate));

Shell commands;

void shell() {
	while(true) {
		CanonicalInput in(requests);
		bool result = dispatch.apply(commands, in);
		requests.next();
		responses.begin();
		CanonicalOutput encoder(responses);
		if (result) {
			int frames = requests.frames();
			encoder << tag("ok", frames);
		} else {
			if(in) {
				encoder << tag("error");
			} else {
				const char* message = in.message();
				encoder << tag("error", message);
			}
		}
		responses.end();
	}
}

int main() {
    console.baud(38400);
    i2c.frequency(400000);
    i2c.start();
    range.init();
    range.startContinuous();

    led1 = true;

    shell();
}
