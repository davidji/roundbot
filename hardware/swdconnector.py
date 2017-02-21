from solid import *
from solid.utils import *
import util
from util import inch_to_mm
from math import sqrt
import boxes
from fixings import M3, M2_5

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
    block = translate([-1, -1, 0])(cube([tenths(rows) + 2, tenths(contacts/rows) + 2, 14]))
    pin = square_hole(tenths(1) - 1, 12)
    pins = union()(*(pin_offset(x, y)(pin) for x in range(rows) for y in range(contacts/rows)))
    void = hole()(square_hole(tenths(1)*1.1, 14))
    voids = union()(*(pin_offset(x, y)(void) for (x, y) in remove))
    return up(14)(rotate([180, 0, 0])(mirror([1,0,0])(block + voids - pins)))

def socket(rows, contacts):
    return translate([-1, -1])(offset(delta=0.6)(square([tenths(rows) + 2, tenths(contacts/rows) + 2])))

# For the nucleo f303re:
#   SWD        | CN7
#   ------------------------
#   RX         | 0,0 | PC10
#   TX         | 1,0 | PC11
#   VDD_TARGET | 0,2 |    
#   SWCLK      | 0,7 | PA14
#   GND        | 1,3 |
#   SWDIO      | 0,6 | PA13
#   NRST       | 1,6 |
#   SWO        | NC
#   5V         | 1,2
NUCLEO_F303RE_PINS = ((0,0), (1,0), (0,2), (0,7), (1,3), (0,6), (1,6), (1,2))

def stlink():
    return header(1, 6, ((0, r) for r in range(5))) + translate([-4, -tenths(4) - 0.8, 0])(header(1,2, ((0,0), (0,1))))

def stlink_socket():
    return socket(1, 6) + (translate([-4, tenths(4) + 0.8])(socket(1,2)))

box = (boxes.builder([25.0,70.0], 2.0, 3.5, 10.0)
       .screw_together(M3)
       .well(translate([7.9,9.55])(rotate([0,0,-90])(stlink_socket())))
       .well(translate([1.2, 32])(socket(1,2)))
       .well(translate([4.6, 58.9])(square([4.0, 3.0])))
       .pinch_mounts(circle(d=3.0), [[6.0, 8.0], [24.0, 8.0], [21.0, 16.0], [22.0, 67.0], [2.5, 63.0]])
       .front(forward(43)(square([4.0, 8.0])))
       .front(forward(41)(left(2)(square([8.0, 12.0]))), thickness=1.0))

def export_scad():
    util.save('nucleo_f303re_swd', header(2, 16, NUCLEO_F303RE_PINS))
    util.save('nucleo_stlink_swd', stlink())
    util.save('nucleo_stlink_socket', stlink_socket())
    util.save('nucleo_stlink_base', box.base().build())
    util.save('nucleo_stlink_lid', box.lid().build())

if __name__ == '__main__':
    export_scad()
