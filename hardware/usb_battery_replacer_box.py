from solid import *
from solid.utils import *
import util
from util import origin, corners, ABIT
from fixings import M3
import boxes
from honeycomb import honeycomb

"""
Box for a micro-usb break out and a buck-boost
converter. There are access holes for the adjustment screw
and terminal screws.

"""

class usb:
    """3mm holes, 8mm back, 9mm apart"""
    d = [13.3,15.9,5.0]
    holes = ([-4.5, -7.5], [4.5, -7.5])
    
class converter:
    """3mm holes 30x46mm"""
    d = [38.0,53.2,14.0]
    dholes = [30, 46]

wall_thickness=2.0
usb_offset = converter.d[1]/2 + 2 + usb.d[1]
side_gap = 2.0
width = converter.d[0] + 2*side_gap
depth = converter.d[1] + usb.d[1] + 2

def usb_box():
    return (boxes.builder([width, depth], 2.0, 6.6, 11)
            .screw_mounts(M3, origin([width/2, converter.d[1]/2])(*corners(*converter.dholes)))
            .screw_mounts(M3, origin([width/2, depth])(*usb.holes))
            .lidVent([20, depth - 30])
            .hole(translate([side_gap + 5.0, 30.2])(circle(d=3)))
            .well(translate([(width-11)/2, -wall_thickness-ABIT])
                   (square([11, 9+wall_thickness+ABIT])))
            .well(translate([width - side_gap - 15.6 - 2, 23.6])(square([2.0, 5.0])), t=0.5)
            .right(usb_port(), center=True))

def usb_box_shoe():
    id = [width, depth, 6.6]
    # I'm leaving a bit of space around the sides to allow convection
    vent = [converter.d[0] - 12, converter.d[1]/2]
    return (
        up(6.6)(forward((wall_thickness + usb.d[1])/2)(
            usb_box().base().build(center=True))) +
        translate([-5, -(converter.d[1]/2)-wall_thickness - ABIT, id[2]])(cube([10, wall_thickness+ABIT, 12])) -
        translate([-7.5/2, usb_offset, id[2]])(cube([7.5, wall_thickness+ABIT, 3])) -
        down(2+ABIT)(linear_extrude(height=2+2*ABIT)(honeycomb(2.0, 1.0, vent[0], vent[1], center=True, inverted=True))))

def usb_port():
    return (back(7.5/2)(
        translate([0.5, 0.5, 0])(offset(r=0.5)(square([1.5, 6.5]))) + 
        square([1.25, 7.5])) +
        left(1.6)(back(7)((square([1.6,14])))))

def usb_box_top():
    id = [width, depth, 11]
    return (forward((wall_thickness + usb.d[1])/2) (
                usb_box().lid().build(center=True)))

if __name__ == '__main__':
    util.save('usb_battery_replacer_shoe', usb_box_shoe())
    util.save('usb_battery_replacer_top', usb_box_top())
