from solid import *
from solid.utils import *

import util
from util import inch_to_mm
from fixings import M2

TENTH=inch_to_mm(0.1)
def tenths(x):
    return inch_to_mm(0.1*x)

HEIGHT=12
WIRE_THICKNESS=1.5
BASE_THICKNESS=2.0
TOLERANCE=0.25

def single_in_line(n):
    return (
        linear_extrude(HEIGHT)(
            square([tenths(n+1)+2.0+TOLERANCE, tenths(1)+2.0+TOLERANCE], center=True)) +
        hole()(up(BASE_THICKNESS)(linear_extrude(HEIGHT)(square([tenths(n+1)+TOLERANCE, tenths(1)+TOLERANCE], center=True))) +
               linear_extrude(BASE_THICKNESS)(
                   square([tenths(n)+WIRE_THICKNESS, WIRE_THICKNESS], center=True) +
                   left(tenths(float(n)/2))(square([tenths(1)+TOLERANCE, tenths(1)+TOLERANCE], center=True)))))

class DualInLine:
    def __init__(self, spacing, n):
        self.spacing = spacing
        self.n = n
        self.d = [spacing+tenths(1)+2.0+TOLERANCE, tenths(n+1)+2.0+TOLERANCE, BASE_THICKNESS+HEIGHT]
        
    def screw_holes(self):
        return util.corners(self.spacing-tenths(1)-6.0, tenths(self.n+1)-2.0)
    
    def base(self):
        return linear_extrude(BASE_THICKNESS)(
                square([self.spacing+tenths(1)+2.0+TOLERANCE, tenths(self.n+1)+2.0+TOLERANCE], center=True) +
                hole()(union()(*(translate(x)(M2.cut()) for x in self.screw_holes()))))
    
    def slots(self):
        single = left(self.spacing/2)(rotate([0,0,90])(single_in_line(self.n)))
        return (single + mirror([1,0,0])(single))
    
    def assembly(self):
        single = left(self.spacing/2)(rotate([0,0,90])(single_in_line(self.n)))
        return self.slots() + self.base()
    
def spacer(n):
    return (
        cube([tenths(n), BASE_THICKNESS, tenths(1)+1.0]) +
        cube([tenths(n), HEIGHT, tenths(1)]) +
        hole()(up(tenths(0.5) - 0.5)(union()(*(
            right(tenths(x+0.5)-0.5)(cube([1.0, HEIGHT, tenths(0.5) + 0.5 + BASE_THICKNESS]))
            for x in range(n))))))

def spacer_collection():
    return (
        union()(*(translate([x*5, 0])(spacer(1)) for x in range(16))) +
        union()(*(translate([x*10, 15])(spacer(2)) for x in range(8))) +
        union()(*(translate([x*20, 30])(spacer(4)) for x in range(4))) +
        union()(*(translate([x*40, 45])(spacer(8)) for x in range(2))))

def export_scad():
    util.save('dupont-15', single_in_line(15))
    util.save('nucleo32', DualInLine(inch_to_mm(0.6), 15).assembly())
    util.save('dupont-spacers', spacer_collection())

if __name__ == '__main__':
    export_scad()
