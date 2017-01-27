from solid import *
from solid.utils import *
import util
from util import radial, pipe

def body(height=21.0, radius=50.0):
    def body_cross_section():
       return translate([radius-1,0])(
            translate([1,0])(polygon(([-3,3], [0, 6], [0,3], [-3,0]))) +
            translate([0, 3])(square([1, height-3])) +
            union()(*(translate([0, y])(polygon([[0,-1],[-1, 0],[0,1]])) 
                      for y in range(7, int(height), 5))) +
            translate([1, height])(polygon(([0,-3],[-3,0],[0,3]))))


    vstrut = left(1.25)(up(3)(cube([2.5,2,height-3])))
    return (rotate_extrude()(body_cross_section()) +
            radial(radius - 3, [+45, -45, +135, -135], 
                   pipe(r=3, t=1.5, h=height)) -
            radial(radius - 3, [a + 7.5 for a in range(0,360,15)], vstrut) -
            radial(radius - 3, [+45, -45, +135, -135], up(height)(cylinder(r=3,h=3))))



if __name__ == '__main__':
    util.save('body', body())