from solid import *
from solid.utils import *

from fixings import M3
from util import corners, inch_to_mm, vadd
import util
import boxes

tenth = inch_to_mm(0.1)
edge_tolerance=0.2

def header(p1, rows, cols):
    return translate([p1[0]-tenth/2, p1[1]-tenth/2])(square([rows*tenth, cols*tenth]))

def usb_port():
    return (back(8.0/2)(
        translate([0.5, 0.5, 0])(offset(r=0.5)(square([1.5, 7.0]))) + 
        square([1.25, 8.0])))
    
def usb_inset():
    return right(1.25)(square([7,12], center=True))

class arduino:
    """This is very similar to nucleo 64. It's just narrower, with one
    more hole."""

    d = [inch_to_mm(2.1) + 2*edge_tolerance ,inch_to_mm(2.7) + 2*edge_tolerance, 6.5]

    """This components centre is the middle of the bounding box around the board.
    This vector is the offset from the corner of the component to the origin in the spec
    """
    origin = [ inch_to_mm(0.1) + edge_tolerance, inch_to_mm(0.2) + edge_tolerance ]

    cn8_p1 = origin
    cn9_p1 = vadd([48.26, 0], origin)
    cn6_p1 = vadd(cn8_p1, [0, tenth*7])
    cn5_p1 = vadd(cn9_p1, [0, tenth*7+4.06])

    holes = [
        vadd(cn6_p1, [0, tenth*7+13.97]),
        vadd(cn5_p1, [0, tenth*9+3.56]),
        vadd(origin, [33.02, -inch_to_mm(0.1)]),
        vadd(origin, [inch_to_mm(0.2), -inch_to_mm(0.1)])]
    
    cn8 = header(cn8_p1, 1, 6)
    cn9 = header(cn9_p1, 1, 8)
    cn6 = header(cn6_p1, 1, 8)
    cn5 = header(cn5_p1, 1, 10)
    icsp = header([inch_to_mm(1.0) + edge_tolerance, inch_to_mm(0.1) + edge_tolerance], 3, 2)

    headers = cn6 + cn8 + hull()(cn5 + cn9)
    power = translate([4.0, d[1] + 2.0 - 15])(square([10, 16]))
    box = (boxes.builder([d[0], d[1]], 2.0, 4.5, d[2])
           .screw_mounts(M3, holes)
           .well(offset(delta=0.25)(headers))
           .well(power)
           .well(offset(delta=0.5)(icsp))
           .right(back(39.0)(usb_port()))
           .right(back(39.0)(usb_inset()), thickness=1.0))

    @staticmethod
    def cut_holes():
        return union()(*(translate(pos)(M3.cut()) for pos in arduino.holes))

if __name__ == '__main__':
    util.save('arduino_base', arduino.box.base().build())
    util.save('arduino_lid', arduino.box.lid().build())