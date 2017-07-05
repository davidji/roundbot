

from solid import *
from solid.utils import *
import util
from util import inch_to_mm, tube, ABIT, corners, pipe

from fixings import M3
from math import tan, radians


"""
Sub-miniature analog joy-sticks.
There's not much useful in documentation of their measurements.
I'm going to treat it like a sphere with a 14mm radius, with a
12mm diameter cylinder sticking out the top.
40 degrees in any direction. The knob on the top is 20mm wide
so the hole in the panel must be at least that wide.
"""

fixing = M3
width=35.0
depth=35.0
pivot_height=9.6
panel_height=11.0
height=pivot_height+panel_height

def block():
    return down(pivot_height+panel_height)(forward(1.8)(linear_extrude(height)(square([35,35], center=True))) -
            up(pivot_height)(sphere(r=14.0)) -
            down(ABIT)(cylinder(h=pivot_height+ABIT, r=14.0)) +
            up(pivot_height)(hole()(cylinder(r1=6.0, r2=6.0 + tan(radians(30.0))*panel_height, h=panel_height))) -
            forward(1.8)(linear_extrude(pivot_height)(square([14.0, depth], center=True))) -
            forward(1.8)(linear_extrude(1.6)(square([25.5, 32.0], center=True))))

def fixings():
    return corners(20.4, 26.6)


def export_scad():
    util.save('joystick-block', block())

if __name__ == '__main__':
    export_scad()
