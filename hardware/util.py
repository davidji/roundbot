from __future__ import division
from solid import *
from solid.utils import *

ABIT=0.1

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

def tube(r, h, ir = None, t = None, center=False):
    return (cylinder(r=r, h=h, center=center) -
            down(ABIT)(cylinder(r=(t and r - t or ir), h=h+2*ABIT)))

def pipe(r, h, ir = None, t = None, center=False):
    """A tube but with first class space"""
    return (cylinder(r=r, h=h, center=center) -
            hole()(down(ABIT)(cylinder(r=(t and r - t or ir), h=h+2*ABIT))))
