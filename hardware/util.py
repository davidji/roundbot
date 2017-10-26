from __future__ import division
from solid import *
from solid.utils import *
import os, os.path
import numpy as np

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

def vadd(a, b):
    return [sum(x) for x in zip(a, b)]

def origin(origin):
    def dotranslate(*points):
        return [ vadd(origin, point) for point in points ]
    return dotranslate

def corners(x, y, z = None, center=True):
    if z:
        return ((x1, y1, z1) for z1 in (center and (z/2, -z/2) or (0, z)) for (x1, y1) in corners(x,y,center=center))
    else:
        return (center and ([x/2, y/2], [x/2, -y/2], [-x/2, -y/2], [-x/2, y/2]) or
                ([x,0], [x,y], [0,y], [0,0]))

class Corner:
    def __init_(self, x = 0, y = 0):
        self.mirror = mirror
    def _side(self, x):
        return Corner(x=x, y=self.y)
    def left(self):
        return _side(1)
    def right(self):
        return _side(0)
    def _end(self, y):
        return Corner(self.x, y)
    def front(self):
        return _end(0)
    def back(self):
        return _end(1)

    def mirror(self):
        return mirror([x,y,0])


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

def stadium(d, r, center=False):
    return hull()(*(translate(p)(circle(r=r)) for p in corners(d[0]-2*r,d[1]-2*r)))

def save(name, assembly):
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, '%s.scad' % name)
    a = assembly
    print("%(name)s: SCAD file written to: \n%(file_out)s" % vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
