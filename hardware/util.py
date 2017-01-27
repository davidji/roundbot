from __future__ import division
from solid import *
from solid.utils import *
import os, os.path

FA=0.1
FS=0.5
ABIT=0.0001

def inch_to_mm(in_inches):
    try:
        i = iter(in_inches)
    except TypeError:
        return in_inches*25.4
    else:
        return [ inch_to_mm(x) for x in i ]


def radial(r, angles, x):
    return union()(*( rotate(a)(forward(r)(x)) for a in angles))

def corner_points(x, y, center=True):
    return (center and ([-x/2, y/2], [x/2, y/2], [x/2, -y/2], [-x/2, -y/2]) or
            ([x,0], [x,y], [0,y], [0,0]))

def corners(d, x, center=True):
    return union()(*(translate(point)(x) for point in corner_points(d[0], d[1], center)))

def tube(h, r = None, ir = None, t = None, center=False):
    r = r or (ir + t)
    ir = ir or (r - t)
    return (cylinder(r=r, h=h, center=center) -
            cylinder(r=ir, h=h, center=center))

def pipe(h, r = None, ir = None, t = None, center=False):
    r = r or (ir + t)
    ir = ir or (r - t)
    """A tube but with first class space"""
    return (cylinder(r=r, h=h, center=center) -
            hole()(cylinder(r=ir, h=h, center=center)))


def save(name, assembly):
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, '%s.scad' % name)
    a = assembly
    print("%(name)s: SCAD file written to: \n%(file_out)s" % vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
