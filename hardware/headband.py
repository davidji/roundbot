from solid import *
from solid.utils import *
import util
from util import *
from math import pi

def headband(r1=64.0, r2=85.0, t=3.0, w=12.0):
    
    combe = right(r1-t/2)(linear_extrude(1)(square([1,1], center=True) + left(0.5)(circle(d=1))))
    combe_spacing = 3.0 # mm
    combe_count = pi*r1/combe_spacing
    combes = union()(*[ rotate([0,0, i*180.0/combe_count])(combe) for i in range(-int(combe_count/2), int(combe_count/2))])
    
    def arcshell(r, ends):
        start, end = ends
        return (arc(rad=r+t/6, start_degrees = start, end_degrees=end) -
                arc(rad=r-t/6, start_degrees = start, end_degrees=end))
    
    return (linear_extrude(w)(
        offset(r=t/3)(
            arcshell(r1, (-90, 90)) +
            forward(r2 - r1)(arcshell(r2, (-130, -90))) +
            back(r2 - r1)(arcshell(r2, (90, 130))))) +
        combes)

def export_scad():
    util.save('headband', headband())

if __name__ == '__main__':
    export_scad()
