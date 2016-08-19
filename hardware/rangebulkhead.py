from __future__ import division

import os, sys

from solid import *
from solid.utils import *
from fixings import M3
from util import *

from sensors import hc_sr04

FA=0.1
FS=0.5

def bulkhead(radius=50.0):
    return (linear_extrude(height=50.0)(arc(radius, -50, +50) - 
                                        square([70, 50], True) -
                                        radial(radius - 3, [+45, -45], M3.cut())) -
            translate([35 - ABIT , 0, 35])(rotate([0, 90, 0])(linear_extrude(height=16)(hc_sr04.tranceiver_cut()))))

def assembly():
    return bulkhead()
 
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'rangebulkhead.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
