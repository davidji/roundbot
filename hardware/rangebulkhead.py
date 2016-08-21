from __future__ import division

import os, sys

from solid import *
from solid.utils import *
from fixings import M3
from util import *

from sensors import hc_sr04
from raspberrypi import aplus

import lego

FA=0.1
FS=0.5

def bulkhead(radius=50.0):
    def rangesensor():
        return translate([radius - 15 - ABIT , 0, 35])(
            rotate([0, 90, 0])(
                linear_extrude(height=16)(hc_sr04.tranceiver_cut())))

    def lego_position(x):
        return translate([radius - 6, 0, lego.pitch+3])(rotate([0, 90, 0])(x))
    electronics = [max([70, aplus.d[0]]), max(50, aplus.d[1])]
    return ((linear_extrude(height=50.0)(
                (arc(radius, -60, +60) -
                 arc(radius-3, -60, -40) -
                 arc(radius-3, +40, +60) -
                 radial(radius-3, [ -45, -135 ], circle(3) + forward(1.5)(square([6,3], True))) -
                 square(electronics, True)) +
                radial(radius-3, [ -45, -135 ], arc(6, 180, 0) - arc(3, 180, 0))) -
            lego_position(linear_extrude(height=10)(lego.surface(2,6))) -
            rangesensor()) +
            lego_position(lego.studs(2,6)) +
            linear_extrude(height=3)(
                arc(radius, -60, +60) - 
                square(electronics, True) -
                radial(radius - 3, [ -45, -135 ], M3.cut())))

def assembly():
    return bulkhead()
 
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'rangebulkhead.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
