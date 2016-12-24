from solid import *
from solid.utils import *
import util
from util import inch_to_mm
from math import sqrt

SQRT2 = sqrt(2.0)

def tenths(x):
    return inch_to_mm(float(x)/10)

def square_hole(x, h):
    return linear_extrude(height=h)(square([x,x], center=True))

def pin_holder(h):
    return linear_extrude(height=h)(
        rotate([0, 0, 45])(
            square([0.5, SQRT2*tenths(1)], center=True) + 
            square([SQRT2*tenths(1), 0.5], center=True)) -
            square([0.8, 0.8], center=True))

def pin_offset(x, y):
    return translate([tenths(0.5 + x), tenths(0.5 + y), 0])

def header(rows, contacts, remove=()):
    block = translate([-1, 0, 0])(cube([tenths(rows) + 2, tenths(contacts/rows), 14]))
    pin = square_hole(tenths(1) - 1, 12)
    pins = union()(*(pin_offset(x, y)(pin) for x in range(rows) for y in range(contacts/rows)))
    void = hole()(square_hole(tenths(1)*1.1, 14))
    voids = union()(*(pin_offset(x, y)(void) for (x, y) in remove))
    return up(14)(rotate([180, 0, 0])(mirror([1,0,0])(block + voids - pins)))

# For the nucleo f303re:
#   SWD        | CN7
#   ------------------------
#   VDD_TARGET | 0,2 |    
#   SWCLK      | 0,7 | PA14
#   GND        | 1,3 |
#   SWDIO      | 0,6 | PA13
#   NRST       | 1,6 |
#   SWO        | NC
#   5V         | 1,2
NUCLEO_F303RE_PINS = ((0,2), (0,7), (1,3), (0,6), (1,6), (1,2))

if __name__ == '__main__':
    util.save('nucleo_f303re_swd', header(2, 18, NUCLEO_F303RE_PINS))
    