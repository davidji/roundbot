
import util
from util import inch_to_mm
from solid import *
from solid.utils import *

"""
This is a little device for bending wire into shapes in tenth of an
inch grid to create 'traces' on prototype board
"""

def former(rows, cols):
    width = inch_to_mm(rows*0.1) + 0.5
    depth = inch_to_mm(cols*0.1) + 0.5
    height = inch_to_mm(0.2)
    return (cube([width, depth, height]) -
            union()(*
                    (right(inch_to_mm(row*0.1))(
                        cube([0.5,depth,1.0]) +
                        cube([0.5, 0.5, height]) +
                        forward(depth - 0.5)(cube([0.5, 1.0, height]))) 
                     for row in range(rows + 1))) -
            union()(*
                    (forward(inch_to_mm(col*0.1))(
                        cube([width, 0.5, 1.0]) +
                        cube([0.5, 0.5, height]) +
                        right(width - 0.5)(cube([0.5, 0.5, height])))
                     for col in range(cols + 1))))
      
if __name__ == '__main__':
    util.save('traceformer', former(12, 12))