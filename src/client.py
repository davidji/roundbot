
DEFAULT_PORT = '/dev/ttyAMA0'
DEFAULT_BAUD = 38400

import serial
from math import pi
import time

class Controller:
    def __init__(self, port = DEFAULT_PORT, baudrate = DEFAULT_BAUD):
        self.serial = serial.Serial(
            port = port,
            baudrate = baudrate,
            xonxoff=False,
            rtscts=False,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = 1)

    def _read_until_ready(self):
        lines = []
        while True:
            line = self.serial.readline()
            if line.startswith("ready"):
                break
            lines.append(line)
        return lines

    def move(self, distance):
        self.serial.write("move {0}\n".format(float(distance)))
        return self._read_until_ready();

    def turn(self, radians):
        self.serial.write("turn {0}\n".format(float(radians)))
        return self._read_until_ready();


    def test(self):
        self.serial.write("test\n")
        return self._read_until_ready()

    def progress(self):
        self.serial.write("progress\n")
        return self._read_until_ready()

    def calibrate(self):
        self.serial.write("progress\n")
        return self._read_until_ready()

controller = Controller('/dev/ttyUSB1')

def track():
    for i in range(10):
        for line in controller.progress():
            print line
        time.sleep(0.1)

for i in range(4):
    print controller.turn(pi/2)
    track()
    controller.move(0.05)
    track()

