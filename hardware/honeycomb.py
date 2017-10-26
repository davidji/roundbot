
from math import sqrt
from solid import *
from solid.utils import *
import util


def hexagon(r):
    """Make a hexagon. The points are on the X axis, and if you put two
    adjacent to each other on the y axis they are 2r apart"""
    R=(2.0*r)/sqrt(3.0)
    halfR=r/sqrt(3.0)
    return polygon([[0, R], [r, halfR], [r, -halfR], [0, -R], [-r, -halfR], [-r, halfR]])

def honeycomb(r, t, w, h, center=False, inverted=False):
    hole = hexagon(r-t/2)
    base = square([w,h])
    R=(2.0*r)/sqrt(3.0)

    def rows():
        if center:
            hrows = int(h/(3.0*R))
            return range(-hrows, hrows + 1)
        else:
            return range(int(h/(1.5*R)))
    
    def cols():
        if center:
            hcols = int(w/(4.0*r))
            return range(-hcols - 1, hcols + 2)
        else:
            return range(int(w/(2.0*r)))

    def holes():
        for row in rows():
            y = 1.5*row*R
            x = row % 2 and r or 0.0
            for col in cols():
                yield translate([x + col*2.0*r, y])(hole)
    bound = square([w, h], center=center)
    return inverted and intersection()(bound, union()(*holes())) or (bound - union()(*holes()))
    

if __name__ == '__main__':
    util.save('honeycomb', honeycomb(1.5, 1.0, 100.0, 100.0, center=True))
